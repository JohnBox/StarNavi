from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from .models import Post, Like
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.user and self.request.user.is_authenticated:
            self.permission_classes = (AuthUserPermission,)
        else:
            self.permission_classes = (AnonUserPermission,)
        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['user_pk'])

    def get_permissions(self):
        if self.request.user and self.request.user.is_authenticated:
            self.permission_classes = (AuthPostPermission,)
        else:
            self.permission_classes = (AnonPostPermission,)
        return super().get_permissions()


class LikeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(post=self.kwargs['post_pk'])

    def get_permissions(self):
        if self.request.user and self.request.user.is_authenticated:
            self.permission_classes = (AuthLikePermission,)
        else:
            self.permission_classes = (AnonLikePermission,)
        return super().get_permissions()


