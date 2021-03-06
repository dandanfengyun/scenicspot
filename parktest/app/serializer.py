from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import SuperAdmin


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class SuperUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperAdmin
        fields = ['user', 'phone']


