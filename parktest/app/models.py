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

    scenic_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='景区名称'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='景区地址'
    )

    scenic_desc = models.TextField(
        verbose_name='景区描述'
    )

    # 各个 网络图片地址逗号隔开。。。其实可以新建图片表关联 景区
    scenic_img = models.TextField(
        verbose_name='景区相关图片'
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        verbose_name = '景点'


class AdminUser(models.Model):
    user = models.OneToOneField(
        User
    )

    scenic_spot = models.ForeignKey(
        ScenicSpot,
        related_name='administrators',
        verbose_name='景区'
    )

    phone = models.CharField(
        max_length=13,
        unique=True
    )

    class Meta:
        verbose_name = '管理员'



