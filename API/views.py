from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import UserSerializer, PostSerializer
from .models import Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['user_pk'])
