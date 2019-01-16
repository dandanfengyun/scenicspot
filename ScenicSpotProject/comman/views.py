import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


# 管理员 员工 用户登录界面
from django.urls import reverse
from rest_framework.generics import ListCreateAPIView

from administrator.models import AdminUser, Staff

admin_cache = caches['admin']
user_cache = caches['user']


# 登陆成功 则是和 管理员相同的套路  话说这应该可以写成一个吧
# 依次查询该用户是否 属于 管理员 员工 游客 如果是 就进入 相应的 视图  可以是重定向或者返回不同数据
# 注  redis 中 token 存储的 是 user id 根据id需要获取到user后
# 进行权限还要进行判断 该 user 是否属于 该  组 对象
class UserLoginAPIView(ListCreateAPIView):

    def get(self, request, *args, **kwargs):

        return HttpResponse('登录界面')

    def post(self, request, *args, **kwargs):
        token = request.session.get('token')

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request=request, username=username, password=password)

        adminuser = AdminUser.objects.filter(user=user).first()
        if adminuser:
            old_user_id = admin_cache.get(token)
            if not (old_user_id == adminuser.user.id):
                token = uuid.uuid4().hex  # 生成随机token  当做 key值
            admin_cache.set(token, adminuser.user.id, settings.ADMIN_USER_ALIVE)  # 一周
            request.session['token'] = token  # 保存到 浏览器中一份
            return redirect(reverse('adminuser:adminindex'))

        staff = Staff.objects.filter(user=user).first()
        if staff:
            old_user_id = user_cache.get(token)
            if not (old_user_id == staff.user.id):
                token = uuid.uuid4().hex  # 生成随机token  当做 key值
            admin_cache.set(token, staff.user.id, settings.ADMIN_USER_ALIVE)  # 一周
            request.session['token'] = token  # 保存到 浏览器中一份
            return redirect(reverse('ticket:staffindex'))

        return HttpResponse('你哪位')
