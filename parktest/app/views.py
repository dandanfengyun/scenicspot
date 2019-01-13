from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializer import *


# 只可注册一次。
class SuperAdminRegister(CreateAPIView):
    serializer_class = UserSerializer

    # def get(self, request, *args, **kwargs):
    #
    #     return Response({'code': 1})

    def create(self, request, *args, **kwargs):
        if SuperAdmin.objects.all().exists():
            return Response({'code': 0, 'msg': '无法注册'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.data.get('username'))
        user.set_password(user.password)
        user.is_superuser = True
        user.save()

        superuser = SuperAdmin.objects.create(user=user, phone=request.data.get('phone'))
        superuserserializer = SuperUserSerializer(superuser)

        return Response(superuserserializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 登录验证 有两次  一次用户名密码。验证成功 则跳转第二个界面
# 根据邮箱验证码再次验证   正常来说应该是手机短信
# class SuperAdminLogin(CreateAPIView):
#     def get(self, request, *args, **kwargs):
#         return Response({'code': 0, 'msg': 'h哈哈'})
#
#     def post(self, request, *args, **kwargs):
#
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(username=username, password=password)
#
        # if user:
        #     # csrf 豁免 出错   问题出在这吗。。。我的哥
        #     login(request, user)
        #     redirect(reverse('app:secondcheck'))

        # return redirect(reverse('app:superlogin'))
#
#         serializer = SuperUserSerializer(user)
#         return Response(serializer.data)
#
#
# class SecondCheckLogin(RetrieveAPIView):
#     def get(self, request, *args, **kwargs):
#         return Response({'cdoe': 0, 'msg': '跳转成功'})

#
# # 超级管理员登录后界面
# class SuperAdminIndex(RetrieveAPIView):
#     pass
#
#
# # 添加景区
# class AddScenicSpot(ListCreateAPIView):
#     def list(self, request, *args, **kwargs):
#         pass
#
#     def create(self, request, *args, **kwargs):
#         pass
#
#
