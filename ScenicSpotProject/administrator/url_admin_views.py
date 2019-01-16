from django.conf.urls import url

from .admin_views import *

# 景点管理员的 操作
urlpatterns = [
    url(r'^adminindex$', AdminUserIndex.as_view(), name='adminindex'),
    url(r'^scenicticket$', ScenicTicketAPIView.as_view(), name='scenicticket'),

    url(r'^staffcreate$', StaffCreateAPIView.as_view(), name='staffcreate'),
    url(r'^staffupdatedestroy$', StaffUpdateDestroyAPIView.as_view(), name='staffupdatedestroy'),
]
