from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class SuperAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperAdmin
        fields = ['user', 'phone']


class ScenicSpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScenicSpot
        fields = ['id', 'name', 'address', 'scenic_img', 'introduction']


class AdminUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminUser
        fields = ['user', 'phone']


# 景区管理员序列化器
class ScenicSpotAdminSerializer(serializers.ModelSerializer):
    adminuser = AdminUserSerializer()

    class Meta:
        model = ScenicSpot
        fields = ['name', 'address', 'adminuser']


# 管理员景区序列化器
class AdminScenicSpotSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    scenicspot = ScenicSpotSerializer()

    class Meta:
        model = AdminUser
        fields = ['user', 'phone', 'scenicspot']

