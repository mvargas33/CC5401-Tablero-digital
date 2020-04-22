from rest_framework import serializers
from .models import PostIt, Board, WorkIn, VoteIn
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


class PostitSerializer(serializers.ModelSerializer):
    stakeholders_vote = serializers.IntegerField(read_only=True)
    developers_vote = serializers.IntegerField(read_only=True)
    class Meta:
        model = PostIt
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class WorkInSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkIn
        fields = '__all__'

    def to_representation(self, obj):
        if type(obj) != WorkIn:
            raise TypeError('obj should be a models.WorkIn instance.')
        return {
            'id': obj.id,
            'board': obj.board.id,
            'user': {
                'id': obj.user.id,
                'username': obj.user.username,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name
            },
            'is_leader': obj.is_leader,
            'team': obj.team,
        }


class AuthenticationSerializer(serializers.Serializer):

    password = serializers.CharField(required=True, write_only=True)
    username = serializers.EmailField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError
        serializer = UserSerializer(user)
        return serializer.data

class VoteInSerializer(serializers.ModelSerializer):
      class Meta:
        model = VoteIn
        fields = '__all__'
