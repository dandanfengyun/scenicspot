from django.conf.urls import url

from app.views import *

urlpatterns = [

    url(r'^superadminregister$', SuperAdminRegister.as_view()),
    # url(r'^superadminlogin$', SuperAdminLogin.as_view(), name='superlogin'),, name='superregister'
    # url(r'^secondchecklogin$', SecondCheckLogin.as_view(), name='secondcheck')
]
