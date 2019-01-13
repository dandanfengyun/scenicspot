from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

# 设置系统环境变量用的是Django的
os.environ.setdefault('DJANGO_SETTING_MODULE', 'scenicspotproject.settings')

app = Celery('mycelery')

app.conf.timezone = 'Asia/Shanghai'

app.config_from_object('django.conf:settings')

# 自动发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

