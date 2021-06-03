from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from comments.views import CommentViewSet
from posts.views import PostViewSet
from unions.views import UnionViewSet
from votes.views import VoteViewSet

router = routers.DefaultRouter()
router.register(r'unions/vote', VoteViewSet)
router.register(r'unions', UnionViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users', include('users.urls')),
    path('admin/', admin.site.urls),
]
