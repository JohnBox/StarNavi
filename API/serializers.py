from django.contrib.auth.models import User
from rest_framework import serializers

from pyhunter import PyHunter
import clearbit

from .models import Post, Like

clearbit.key = 'sk_7cf5e2e645cbe27d9c4f865aef594142'

hunter = PyHunter('b6d0ce8c8da73db68946e7ae3743b4327ef8b5d8')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    posts = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'posts')

    def create(self, validated_data):
        try:
            verify = hunter.email_verifier(validated_data['email'])
        except:
            verify = None
        if verify and verify['result'] == 'invalid':
            raise serializers.ValidationError('Invalid email')
        try:
            found = clearbit.Enrichment.find(email=validated_data['email'])
        except:
            found = None
        if found:
            person = found['person']['name']
            validated_data['first_name'] = validated_data.get('first_name') or person['givenName']
            validated_data['last_name'] = validated_data.get('last_name') or person['familyName']
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created', 'likes')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post')
