from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from unionImages.views import UnionImagesViewSet
from comments.views import CommentViewSet
from posts.views import PostViewSet
from unions.views import UnionViewSet
from votes.views import VoteViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'unions/vote', VoteViewSet)
router.register(r'unions/images', UnionImagesViewSet)
router.register(r'unions', UnionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users', include('users.urls')),
    path('unions', include('unions.urls')),
    path('admin/', admin.site.urls),
]
