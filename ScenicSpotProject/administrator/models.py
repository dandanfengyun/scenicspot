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


class ScenicSpot(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='景点名',
    )

    address = models.CharField(
        max_length=255,
        verbose_name='景点位置',
    )

    scenic_img = models.CharField(
        max_length=255,
        verbose_name='相关图片',
    )

    introduction = models.TextField(
        verbose_name='景点介绍'
    )

    class Meta:
        verbose_name = '景点'


# 与景点也是一对一的关系
class AdminUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='adminuser'
    )

    phone = models.CharField(
        max_length=13,
        verbose_name='手机',
    )

    scenicspot = models.OneToOneField(
        ScenicSpot,
        on_delete=models.CASCADE,
        related_name='adminuser'
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = '管理员'
