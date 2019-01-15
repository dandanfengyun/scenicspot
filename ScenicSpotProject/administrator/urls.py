from django.conf.urls import url

from .views import *


# 超级管理员的操作
urlpatterns = [

    url(r'^superadminregister$', SuperAdminRegister.as_view(), name='superadminregister'),
    url(r'^superadminlogin$', SuperAdminLogin.as_view(), name='superadminlogin'),

    url(r'^superadminindex$', SuperAdminIndexAPIView.as_view(), name='superadminindex'),

    url(r'^scenicspotcreate$', ScenicSpotCreateAPIView.as_view(), name='scenicspot'),
    url(r'scenicupdatedestroy$', ScenicUpdateDestroyAPIView.as_view(), name='scenicupdatedestroy'),

    url(r'^adminusercreate$', AdminUserCreateAPIView.as_view(), name='adminusercreate'),
    url(r'^adminupdatedestroy$', AdminUserUpdateDestroyAPIView.as_view(), name='adminupdatedestroy'),

]
