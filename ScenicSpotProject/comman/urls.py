from django.conf.urls import url

from .views import UserLoginAPIView

urlpatterns = [
    url(r'^userlogin$', UserLoginAPIView.as_view(), name='userlogin')
]
