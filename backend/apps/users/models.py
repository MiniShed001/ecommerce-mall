from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户：继承 Django 自带 User，追加手机号/头像/昵称"""
    phone = models.CharField('手机号', max_length=20, blank=True, default='')
    avatar = models.URLField('头像', blank=True, default='')
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    created_at = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        db_table = 'mall_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
