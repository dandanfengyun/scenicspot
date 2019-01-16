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

    is_adminuser = models.BooleanField(
        default=True,
        verbose_name='是否为管理员',
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


class ScenicTicket(models.Model):
    scenic = models.ForeignKey(
        ScenicSpot,
        related_name='scenic_tickets',
        on_delete=models.CASCADE,
        verbose_name='景区',
    )
    ticket_price = models.FloatField(
        default=40.0,
        verbose_name='票价',
    )
    tickets_one_day = models.IntegerField(
        default=10000,
        verbose_name='每日限流',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='票价信息规定时间',
    )
    is_opened = models.BooleanField(
        default=True,
        verbose_name='是否开放'
    )
    is_used = models.BooleanField(
        default=True,
        verbose_name='是否有效'
    )

    class Meta:
        verbose_name = '景点相关信息'


# 员工 可以扩展工号属性
class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff'
    )

    scenicspot = models.ForeignKey(
        ScenicSpot,
        related_name='staff',
        on_delete=models.CASCADE,
        verbose_name='所属景点'
    )

    phone = models.CharField(
        max_length=13,
        verbose_name='手机',
    )

    create_time = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = '员工'
