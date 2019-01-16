import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import caches
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.utils import json


from .myauth import AdminUserAuth
from .permission import AdminUserPermission
from .serializer import ScenicSpotSerializer, ScenicSpot, ScenicSpotTicketSerializer, UserSerializer, StaffSerializer
from .models import AdminUser, ScenicTicket, Staff


admin_cache = caches['admin']


# 管理员主页  只有所管理的景点信息 可通过该界面 跳转到其他界面
# 如 修改票价  修改每日票数
class AdminUserIndex(RetrieveAPIView):
    serializer_class = ScenicSpotSerializer
    queryset = ScenicSpot.objects.all()

    authentication_classes = (AdminUserAuth,)
    permission_classes = (AdminUserPermission,)

    def get(self, request, *args, **kwargs):
        adminuser = request.user
        instance = adminuser.scenicspot
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

        # imgpaths = ['img/KDA.jpg', 'img/shilan.jpg', 'img/yan.jpg']
        # return render(request, 'adminuser/index.html', context={'imgpaths': imgpaths})


# 景区门票相关信息
class ScenicTicketAPIView(ListCreateAPIView):

    serializer_class = ScenicSpotTicketSerializer

    authentication_classes = (AdminUserAuth,)
    permission_classes = (AdminUserPermission,)

    def get(self, request, *args, **kwargs):
        adminuser = request.user
        scenic_spot = adminuser.scenicspot

        # 如果查询到 景区相关门票信息 且 正在使用
        scenic_ticket = ScenicTicket.objects.filter(Q(scenic=scenic_spot) & Q(is_used=True)).first()
        if scenic_ticket:
            queryset = scenic_ticket
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        return Response({'code': 0, 'msg': '添加景点相关门票信息'})

    def create(self, request, *args, **kwargs):
        adminuser = request.user
        scenic_spot = adminuser.scenicspot

        # 如果查询到 景区相关门票信息 且 正在使用  就将使用置为 False
        scenic_ticket = ScenicTicket.objects.filter(Q(scenic=scenic_spot) & Q(is_used=True)).first()
        if scenic_ticket:
            scenic_ticket.is_used = False
            scenic_ticket.save()

        ticket_price = request.data.get('ticket_price', 40)
        tickets_one_day = request.data.get('tickets_one_day', 10000)
        is_opened = request.data.get('is_opened', True)

        scenic_ticket = ScenicTicket.objects.create(scenic=scenic_spot, ticket_price=ticket_price, tickets_one_day=tickets_one_day,
                                                    is_opened=is_opened)

        serializer = self.get_serializer(scenic_ticket)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 添加 员工信息
class StaffCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

    authentication_classes = (AdminUserAuth,)
    permission_classes = (AdminUserPermission,)

    def get(self, request, *args, **kwargs):
        scenicspot = request.user.scenicspot

        staffes = Staff.objects.filter(scenicspot=scenicspot)
        if staffes:
            serializer = StaffSerializer(staffes, many=True)
            return Response(serializer.data)

        return HttpResponse('添加员工界面')

    def post(self, request, *args, **kwargs):
        admin_user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.data.get('username'))
        user.set_password(user.password)
        user.is_staff = True
        user.save()

        scenicspot = admin_user.scenicspot

        staff = Staff.objects.create(user=user, scenicspot=scenicspot, phone=request.data.get('phone'))

        new_serializer = StaffSerializer(instance=staff)

        return Response(new_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 员工 修改 删除
class StaffUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = StaffSerializer

    authentication_classes = (AdminUserAuth,)
    permission_classes = (AdminUserPermission,)

    def get(self, request, *args, **kwargs):
        scenicspot = request.user.scenicspot

        staffes = Staff.objects.filter(scenicspot=scenicspot)
        if staffes:
            serializer = StaffSerializer(staffes, many=True)
            return Response(serializer.data)

        return HttpResponse('添加员工界面')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        adminuser = request.user

        staff_id = int(request.data.get('staff_id', 0))
        # 根据 景区  所属员工信息中查询
        instance = adminuser.scenicspot.staff.all().filter(id=staff_id).first()
        if not instance:
            return HttpResponse('未选择员工信息就不要修改了啊')

        serializer = UserSerializer(instance.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.user.set_password(instance.user.password)
        instance.user.save()

        phone = request.data.get('phone', instance.phone)
        instance.phone = phone
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        new_serializer = StaffSerializer(instance)
        return Response(new_serializer.data)

    def delete(self, request, *args, **kwargs):

        adminuser = request.user

        staff_id = int(request.data.get('staff_id', 0))
        # 根据 景区  所属员工信息中查询
        instance = adminuser.scenicspot.staff.all().filter(id=staff_id).first()
        if not instance:
            return HttpResponse('不可删除或者改员工不存在')

        user = instance.user
        self.perform_destroy(instance)
        user.delete()      # 删除掉user表中信息
        return Response(data={'code': 204, 'msg': '删除成功'}, status=status.HTTP_204_NO_CONTENT)

