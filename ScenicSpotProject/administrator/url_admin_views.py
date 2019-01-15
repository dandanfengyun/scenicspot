from django.conf.urls import url

from .admin_views import *

# 景点管理员的 操作
urlpatterns = [
    url(r'^adminlogin$', AdminLoginAPIView.as_view(), name='adminlogin'),
    url(r'^adminindex$', AdminUserIndex.as_view(), name='adminindex'),

]
