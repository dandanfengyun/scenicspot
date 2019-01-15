import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.utils import json

from .myauth import AdminUserAuth
from .serializer import ScenicSpotSerializer, ScenicSpot
from .models import AdminUser


user_cache = caches['user']

class AdminLoginAPIView(ListCreateAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):

        return HttpResponse('管理员登录界面')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request=request, username=username, password=password)
        adminuser = AdminUser.objects.filter(user=user).first()
        if adminuser:
            token = request.session.get('token')
            old_admin_id = user_cache.get(token)
            if not (old_admin_id == adminuser.id):
                # 同超级管理员一样  不过 不需要 验证码 验证了
                token = uuid.uuid4().hex    # 生成随机token  当做 key值
                user_cache.set(token, adminuser.id, settings.ADMIN_USER_ALIVE)  # 一周
                request.session['token'] = token    # 保存到 浏览器中一份

            return redirect(reverse('adminuser:adminindex'))
        return HttpResponse('你哪位')


class AdminUserIndex(RetrieveAPIView):
    serializer_class = ScenicSpotSerializer
    queryset = ScenicSpot.objects.all()

    # authentication_classes = (AdminUserAuth,)

    def get(self, request, *args, **kwargs):
        # adminuser = request.user
        adminuser = AdminUser.objects.first()
        if isinstance(adminuser, AnonymousUser):
            return HttpResponse('请登录')
        instance = adminuser.scenicspot
        serializer = self.get_serializer(instance)

        print(serializer.data)

        return render(request, 'adminuser/index.html')

