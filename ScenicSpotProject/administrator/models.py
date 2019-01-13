from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class SuperAdmin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='superadmin'
    )

    phone = models.CharField(
        max_length=13,
        verbose_name='手机',
    )

    create_time = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = '超级管理员'

'''
class AdminUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='superadmin'
    )

    phone = models.CharField(
        max_length=13,
        verbose_name='手机',
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = '管理员'
'''


class ScenicSpot(models.Model):

    class Meta:
        verbose_name = '景点'
