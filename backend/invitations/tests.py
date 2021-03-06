# Create your tests here.
from django.db.models import QuerySet
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer
from users.models import User
from unions.models import Union, UnionUsers
import json


class InvitationTests(APITestCase):
    def perform_request(self, user: User, name):
        data = {
            "name": name
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)
        req = self.client.post('/unions/invite', data, format='json')
        content_unicode = req.content.decode('utf-8')
        response_body = json.loads(content_unicode)

        return req, response_body

    def setUp(self):
        self.client = APIClient()
        self.koen: User = User.objects.create_user("koen@hva.nl", "koen")
        self.teun: User = User.objects.create_user("teun@hva.nl", "teun")
        self.user_alone: User = User.objects.create_user("alone@hva.nl", "alone")
        self.union: Union = Union.objects.create(name="Crypto", description="Bitcoin", members_can_invite=True,
                                                 creator=self.koen)

        UnionUsers.objects.create(union=self.union, user=self.koen)
        self.union_members_cant_invite: Union = Union.objects.create(
            name="Crypto SECRET", description="Bitcoin",
            members_can_invite=False, creator=self.koen)
        UnionUsers.objects.create(union=self.union_members_cant_invite, user=self.teun)
        UnionUsers.objects.create(union=self.union_members_cant_invite,
                                  user=self.koen)  # Koen is admin so should be here

    def test_create_invitation_endpoint(self):
        res, res_body = self.perform_request(self.koen, self.union.name)

        created_invite: Invitation = Invitation.objects.first()

        # Invitation creation
        self.assertEqual(len(Invitation.objects.all()), 1)
        self.assertEqual(
            created_invite.invite_creator.user_id, self.koen.user_id)
        self.assertEqual(created_invite.union.name, self.union.name)
        # Response
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue("invite_token" in res_body)
        self.assertEqual(res_body["invite_token"], created_invite.token)

    def test_create_with_invalid_union(self):
        res, res_body = self.perform_request(self.koen, 9999)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue("The given union does not exist" in str(res_body))

    def test_create_with_user_not_in_union(self):
        # Before we start lets make sure that test user Teun has access to the union
        union_users: QuerySet[User] = self.union_members_cant_invite.users.all()
        self.assertTrue(len(union_users.filter(user_id=self.user_alone.user_id)) == 0)

        res, res_body = self.perform_request(
            self.user_alone, self.union_members_cant_invite.name)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            "This user cannot create an invite for this union" in str(res_body))

    def test_create_when_members_cant_invite(self):
        # Teun is user & Koen is Admin -> members can't invite
        union_users: QuerySet[User] = self.union_members_cant_invite.users.all()
        self.assertTrue(len(union_users.filter(user_id=self.teun.user_id)) == 1)
        self.assertEqual(self.union_members_cant_invite.creator.user_id, self.koen.user_id)

        # Member teun tries generating invite which only the admin can do
        res, res_body = self.perform_request(
            self.teun, self.union_members_cant_invite.name)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            "Only the admin can invite for this union" in str(res_body))

    def test_create_from_admin_regardless_of_invite_setting(self):
        # Koen is Admin -> members can't invite
        union_users: QuerySet[User] = self.union_members_cant_invite.users.all()
        self.assertTrue(len(union_users.filter(user_id=self.koen.user_id)) == 1)
        self.assertEqual(self.union_members_cant_invite.creator.user_id, self.koen.user_id)  # Koen is Admin
        self.assertFalse(self.union_members_cant_invite.members_can_invite)  # Union has setting set to False

        # Admin Koen teun tries generating invite for members_cant_invite union
        res, res_body = self.perform_request(
            self.koen, self.union_members_cant_invite.name)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Koen is Admin -> members CAN invite
        union_users: QuerySet[User] = self.union.users.all()
        self.assertTrue(len(union_users.filter(user_id=self.koen.user_id)) == 1)
        self.assertEqual(self.union.creator.user_id, self.koen.user_id)  # Koen is Admin
        self.assertTrue(self.union.members_can_invite)  # Union has setting set to True

        # Admin Koen teun tries generating invite for members_cant_invite union
        res, res_body = self.perform_request(
            self.koen, self.union.name)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_when_no_invites_left_for_union(self):
        self.perform_request(self.koen, self.union.name)
        self.perform_request(self.koen, self.union.name)
        res, res_body = self.perform_request(self.koen, self.union.name)  # 1 to many

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue("This user has no invites left" in str(res_body))

    def test_invite_details(self):
        self.perform_request(self.koen, self.union.name)
        created_invite: Invitation = Invitation.objects.first()

        data = {
            "invite_token": created_invite.token
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.koen.token)
        res = self.client.get('/unions/invite', data, format='json')
        res_body = json.loads(res.content.decode('utf-8'))

        self.assertTrue("union" in res_body)
        self.assertTrue("invite_creator" in res_body)
        self.assertTrue("token" in res_body)
        self.assertTrue("status" in res_body)

        self.assertEqual(res_body['union']['name'], created_invite.union.name)
        self.assertEqual(res_body['invite_creator']['username'], created_invite.invite_creator.username)

    def test_invite_details_not_found(self):
        self.perform_request(self.koen, self.union.name)
        data = {
            "invite_token": "9999"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.koen.token)
        res = self.client.get('/unions/invite', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_invite_details_bad_request(self):
        self.perform_request(self.koen, self.union.name)
        data = {
            "bad": "9999"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.koen.token)
        res = self.client.get('/unions/invite', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class InvitationAcceptTests(APITestCase):
    def perform_request(self, user: User, invite_token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)
        req = self.client.post(
            f'/unions/invite/accept?invite_token={invite_token}', format='json')
        content_unicode = req.content.decode('utf-8')
        response_body = json.loads(content_unicode)

        return req, response_body

    def setUp(self):
        self.client = APIClient()
        self.koen: User = User.objects.create_user("koen@hva.nl", "koen")
        self.teun: User = User.objects.create_user("teun@hva.nl", "teun")
        self.union: Union = Union.objects.create(name="Crypto", description="Bitcoin", members_can_invite=True,
                                                 creator=self.koen)

        UnionUsers.objects.create(union=self.union, user=self.teun)

        # Creating via serializer because it needs a token
        data = {
            "invite_creator": self.teun.user_id,
            "union": self.union.name
        }
        ser = InvitationCreateSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        self.invitation_data = ser.data

    def test_simple_accept(self):
        res, res_body = self.perform_request(
            self.koen, self.invitation_data['invite_token'])
        invite: Invitation = Invitation.objects.filter(
            token=self.invitation_data['invite_token']).first()

        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue("name" in res_body)
        self.assertEqual(res_body["name"], invite.union.name)
        self.assertIsNotNone(invite.accepted_at)
        self.assertEqual(invite.invite_acceptor, self.koen)

    def test_bad_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.koen.token)

        res = self.client.post(f'/unions/invite/accept', format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(
            f'/unions/invite/accept?invitation_token', format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(
            f'/unions/invite/accept?invitation_token=', format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(f'/unions/invite/accept?token=', format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(
            f'/unions/invite/accept?invite_token=aasdfsadf', format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_invite_already_used(self):
        # Accept our own invite
        self.perform_request(self.koen, self.invitation_data['invite_token'])
        # Try to use invitation again
        res, res_body = self.perform_request(
            self.koen, self.invitation_data['invite_token'])

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_body, ['This invite has already been accepted'])
