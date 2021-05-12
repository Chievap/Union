from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.backends import JWTAuthentication
from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer, InvitationSerializer


class InvitationsAPIView(APIView):
    serializer_class = InvitationCreateSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.data)
        invitation = Invitation.objects.get(token="6787d064-b174-11eb-8f7d-0242ac140004")

        serializer = InvitationSerializer(invitation)

        # TODO: Check for permissions
        # TODO: Error handling

        return Response(serializer.data)

    def post(self, request):
        try:
            union_id = request.data['union_id']
        except KeyError:
            return Response({'errors': "Missing union_id key"}, status=status.HTTP_400_BAD_REQUEST)

        user, token = JWTAuthentication.authenticate_credentials_from_request_header(request)

        creation_data = {
            'union': union_id,
            'invite_creator': user.user_id
        }

        serializer = self.serializer_class(data=creation_data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            if type(e) is PermissionError:
                return Response(str(e), status=status.HTTP_403_FORBIDDEN)
            elif type(e) is ValidationError:
                if "does not exist" in str(e):
                    return Response(str(e), status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

            # Error went through all catches
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.save()
        serialized_data = serializer.data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class InvitationsAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            parsed_token = request.GET['invite_token']
            if parsed_token == "":
                raise ValueError
        except (MultiValueDictKeyError, ValueError):
            return Response({"The invite_token query params is missing/incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        invite_token = request.GET['invite_token']
        database_invitation: Invitation = Invitation.objects.filter(token=invite_token).first()

        if database_invitation is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        if not database_invitation.can_be_accepted():
            return Response({"This invite has already been accepted"},
                            status=status.HTTP_403_FORBIDDEN)

        # Check for archived union if we want to implement it

        user, token = JWTAuthentication.authenticate_credentials_from_request_header(request)

        # Add user to unions
        InvitationSerializer.accept_invitation(database_invitation, user)

        return Response({}, status=status.HTTP_202_ACCEPTED)
