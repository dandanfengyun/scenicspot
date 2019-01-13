import time
from celery import task
from django.conf import settings
from django.core.mail import send_mail


@task
def task_one(i):
    print(i)
    print(4)
    time.sleep(4)
    print('执行完毕')
    return 'OK'


@task
def send_check_code(email, code):
    title = '验证码'
    message = '验证码是 %s一分钟内有效>' % code
    from_email = settings.DEFAULT_FROM_EMAIL
    receives = [
        email,
    ]
    send_mail(title, message, from_email, receives)
    print('发送完成')
