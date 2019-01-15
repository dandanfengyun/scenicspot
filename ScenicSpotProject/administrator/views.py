import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


from .until import generate_code
from .myauth import SuperAdminAuth
from .mythrottles import MyThrottles
from .permission import SuperAdminPermission
from .models import SuperAdmin
from .serializer import *
from .tasks import send_code

user_cache = caches['user']


# 只可注册一次。
class SuperAdminRegister(ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        return Response({'code': 1, 'msg': '假装注册页面'})

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
        superuserserializer = SuperAdminSerializer(superuser)

        return Response(superuserserializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 使用该接口时直接向 管理员邮箱发送验证码。登录必须验证验证码
# 为防止 其他人  误访问  其实应该有限制只对 而且  应该是点击按钮才会发送。。。
# 应该是手机发送  而不是邮箱验证码
# 可以加个 节流设置 一天只准 访问 5次 之类  如果是真正管理员  不至于 访问五次登不进去
class SuperAdminLogin(ListCreateAPIView):
    serializer_class = SuperAdminSerializer

    # throttle_classes = (MyThrottles, )

    def get(self, request, *args, **kwargs):
        code = generate_code()
        send_code.delay('2942035955@qq.com', code)
        # 保存到缓存一份
        user_cache.set('check_code', code, 60*5)     # 五分钟失效
        return Response(data={'code': 1, 'msg': '假装登录页面'})

    def post(self, request, *args, **kwargs):
        # 验证验证码
        # 如果验证码 不同  则可能验证码过期  或者 其他人无意访问到该网址
        post_code = request.data.get('code')
        if not post_code:
            return HttpResponse('error')

        real_code = user_cache.get('check_code')
        if post_code != real_code:
            print(post_code)
            return HttpResponse('请重新输入验证码')

        username = request.data.get('username')
        password = request.data.get('password')
        # 自定义验证 可以使用 用户名密码 邮箱登录
        user = authenticate(request=request, username=username, password=password)
        superadmin = SuperAdmin.objects.filter(user=user).first()
        if superadmin:
            token = uuid.uuid4().hex    # 生成随机token  当做 key值
            # redis缓存中 token 当做 key 值  保存 用户 id
            user_cache.set(token, superadmin.id, settings.SUPER_ADMIN_ALIVE)
            request.session['token'] = token    # 保存到 浏览器中一份

            return redirect(reverse('administrator:superadminindex'))

        return HttpResponse('登录入口出错')


# 主页展示
class SuperAdminIndexAPIView(ListAPIView):
    serializer_class = ScenicSpotAdminSerializer
    queryset = ScenicSpot.objects.all()

    authentication_classes = (SuperAdminAuth,)
    permission_classes = (SuperAdminPermission,)

    def list(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'code': 1, 'msg': '未登录'})

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if not queryset:
            return Response({'code': 1, 'msg': '无数据'})

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


# 添加景点
class ScenicSpotCreateAPIView(CreateAPIView):
    serializer_class = ScenicSpotSerializer

    authentication_classes = (SuperAdminAuth,)
    permission_classes = (SuperAdminPermission,)

    def get(self, request, *args, **kwargs):

        return HttpResponse('添加景点界面')

    def post(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'code': 1, 'msg': '未登录'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 点击景点信息右侧进入详情页  可 修改 删除
class ScenicUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ScenicSpotSerializer

    authentication_classes = (SuperAdminAuth,)
    permission_classes = (SuperAdminPermission,)

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'code': 1, 'msg': '未登录'})

        scenic_id = int(request.query_params.get('scenic_id'))
        instance = ScenicSpot.objects.get(pk=scenic_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 直接重写 update 就可以完成 update patch的返回
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        scenic_id = int(request.query_params.get('scenic_id'))
        instance = ScenicSpot.objects.get(pk=scenic_id)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):

        scenic_id = request.query_params.get('scenic_id')
        instance = ScenicSpot.objects.get(pk=scenic_id)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 添加管理员信息  界面应该有所有 没有管理员的景点名称及ID
class AdminUserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

    authentication_classes = (SuperAdminAuth,)
    permission_classes = (SuperAdminPermission,)

    def get(self, request, *args, **kwargs):

        # 获取到所有未 有 管理员的 景区  只有 未有管理员的景区才能创建时加入
        instances = ScenicSpot.objects.filter(adminuser=None)

        if instances.count() == 0:
            return Response({'code':  1, 'msg': '所有景区都已经有管理员了。。如果想要添加新的管理员 请取消一个管理员的职位'})
        for instance in instances:
            print(instance.name)

        return HttpResponse('添加景点界面')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.data.get('username'))
        user.set_password(user.password)
        user.save()

        scenic_id = int(request.data.get('scenic_id'))
        admin_user = AdminUser.objects.create(user=user, phone=request.data.get('phone'), scenicspot_id=scenic_id)

        new_serializer = AdminScenicSpotSerializer(instance=admin_user)

        return Response(new_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 管理员 修改 删除
class AdminUserUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = AdminScenicSpotSerializer

    authentication_classes = (SuperAdminAuth,)
    permission_classes = (SuperAdminPermission,)

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'code': 1, 'msg': '未登录'})

        admin_id = int(request.query_params.get('admin_id'))
        instance = AdminUser.objects.get(pk=admin_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        admin_id = int(request.data.get('admin_id'))
        adminuser = AdminUser.objects.get(pk=admin_id)
        instance = adminuser.user

        serializer = UserSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        scenicspot_id = request.data.get('scenic_id')
        if scenicspot_id:
            adminuser.scenicspot_id = int(scenicspot_id)
            adminuser.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        new_serializer = AdminScenicSpotSerializer(adminuser)
        return Response(new_serializer.data)

    def delete(self, request, *args, **kwargs):
        admin_id = request.data.get('admin_id')
        instance = AdminUser.objects.get(pk=admin_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


