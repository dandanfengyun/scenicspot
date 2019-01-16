from django.conf.urls import url

from ticket.views import *

urlpatterns = [
    url(r'^staffindex$', StaffIndexAPIView.as_view(), name='staffindex'),
]
