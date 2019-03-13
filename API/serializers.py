from django.contrib.auth.models import User
from rest_framework import serializers

from pyhunter import PyHunter
import clearbit

from .models import Post, Like

clearbit.key = 'sk_7cf5e2e645cbe27d9c4f865aef594142'

hunter = PyHunter('b6d0ce8c8da73db68946e7ae3743b4327ef8b5d8')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'email': {'required': True}}

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
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created')

    def create(self, validated_data):
        post = Post.objects.create(user=self.context['user'], **validated_data)
        return post


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post')

    def create(self, validated_data):
        like = Like.objects.create(user=self.context['user'], 
                                   post=Post.objects.get(pk=self.context['post_pk']))
        return like
    
    def validate(self, attrs):
        try:
            Like.objects.get(user=self.context['user'],
                             post=Post.objects.get(pk=self.context['post_pk']))
        except:
            return {}
        else:
            raise serializers.ValidationError('like already created')
