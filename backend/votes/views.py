from django.db.models import QuerySet
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from authentication.backends import JWTAuthentication
from comments.models import Comment
from posts.models import Post
from votes.serializer import VoteSerializer
from votes.models import Vote, VoteENUM, updatePostOrCommentOnVote


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def create(self, request, *args, **kwargs):
        user, token = JWTAuthentication.authenticate_credentials_from_request_header(
            request)
        votes: QuerySet[Vote]

        if token is None or user is None:
            return Response("Unauthorized user", status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = user.user_id

        if 'post' not in request.data:
            return Response("Post id is required", status=status.HTTP_400_BAD_REQUEST)

        if 'comment' in request.data:
            votes = Vote.objects.filter(
                post=request.data['post'], comment=request.data['comment'], user=user.user_id)
        else:
            votes = Vote.objects.filter(
                post=request.data['post'], comment=None, user=user.user_id)

        if votes.count() != 0:
            old = votes[0].vote
            new = request.data['vote']

            serializer = self.serializer_class(
                votes[0],
                data={"vote": request.data['vote']},
                partial='partial'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if 'comment' in request.data:
                # Vote model is saved, lets update its post model.
                comment = Comment.objects.get(comment_id=request.data['comment'])
                comment = updatePostOrCommentOnVote(old, new, comment)
                comment.save()
            else:
                # Vote model is saved, lets update its post model.
                post = Post.objects.get(post_id=request.data['post'])
                post = updatePostOrCommentOnVote(old, new, post)
                post.save()

            return Response(serializer.data, status.HTTP_200_OK)

        # Validate and save according to serializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Vote model is saved, lets update its model.
        new = request.data['vote']

        if 'comment' in request.data:
            # Vote model is saved, lets update its post model.
            comment = Comment.objects.get(comment_id=request.data['comment'])
            comment = updatePostOrCommentOnVote(VoteENUM.NEUTRAL, new, comment)
            comment.save()
        else:
            # Vote model is saved, lets update its post model.
            post = Post.objects.get(post_id=request.data['post'])
            post = updatePostOrCommentOnVote(VoteENUM.NEUTRAL, new, post)
            post.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
