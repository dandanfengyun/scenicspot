import time
from celery import task
from django.conf import settings
from django.core.mail import send_mail


@task
def task_one(i):
    print(i)
    time.sleep(i)
    print('执行完毕')
    return 'OK'


@task
def send_code(email_address, code):
    title = '登录验证码'
    message = '验证码是: %s 五分钟内有效' % code
    from_email = settings.DEFAULT_FROM_EMAIL
    receives = [
        email_address,
    ]

    send_mail(title, message, from_email, receives)
    print('发送完成')

