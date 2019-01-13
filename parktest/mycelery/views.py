import time

from django.conf import settings
from django.core.cache import caches
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from mycelery.unitl import generate_code
from .tasks import task_one, send_check_code

cache = caches['default']


def test_celery(request):
    res = task_one.delay(4)
    # print(res)
    return HttpResponse('OK')


def test_email(request):
    time.sleep(4)

    title = '自己写给自己'
    message = '好好学'
    from_email = settings.DEFAULT_FROM_EMAIL
    receives = [
        '2942035955@qq.com',
        '2760483212@qq.com'
    ]
    send_mail(subject=title, message=message, from_email=from_email, recipient_list=receives)

    return HttpResponse('发送成功')


def celery_send(request):
    code = generate_code()
    cache.set('code', code, 60*5)
    send_check_code.delay('2942035955@qq.com', code)
    return HttpResponse('发送成功')


def check_code(request):
    if request.method == 'GET':
        return HttpResponse('哈哈哈')

    if request.method == 'POST':
        code = cache.get('code')
        send_code = request.POST.get('code')
        if code == send_code:
            return HttpResponse('验证成功')
        return HttpResponse('验证失败')
