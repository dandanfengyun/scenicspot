from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^superadminregister$', SuperAdminRegister.as_view(), name='superadminregister'),
    url(r'^superadminlogin$', SuperAdminLogin.as_view(), name='superadminlogin'),

    url(r'^scenicspot$', ScenicSpotAPIView.as_view(), name='scenicspot'),

    # url(r'^testcelery$', test_celery),
]
