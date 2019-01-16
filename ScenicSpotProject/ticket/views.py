from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from administrator.models import Staff
from .myauth import StaffAuth
from .mypermission import StaffPermission


class StaffIndexAPIView(ListCreateAPIView):

    authentication_classes = (StaffAuth,)
    permission_classes = (StaffPermission,)

    def get(self, request, *args, **kwargs):

        return HttpResponse('售票界面')

    def post(self, request, *args, **kwargs):

        return HttpResponse('尚未完成')
