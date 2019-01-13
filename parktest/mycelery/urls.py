from django.conf.urls import url

from .views import *

urlpatterns = [
    url('^test/', test_celery),
    url('testmail/', test_email),
    url(r'celerysend/', celery_send),
    url(r'checkcode$', check_code),

]
