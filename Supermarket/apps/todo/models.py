from django.core.validators import RegexValidator
from django.db import models

from db.base_model import BaseModel


class User(BaseModel):
    sex_choices = (
        (1, '男'),
        (2, '女'),
    )

    username = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    password = models.CharField(max_length=32, verbose_name='密码')
    telephone = models.CharField(max_length=11,
                                 verbose_name='手机号',
                                 validators=[RegexValidator(r'^1[3-9]\d{9}$', "请输入正确的号码"),
                                             ])
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    sex = models.SmallIntegerField(choices=sex_choices, default=1, verbose_name='性别')
    school = models.CharField(max_length=50, null=True, blank=True, verbose_name='学校名')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='现居地址')
    hometown = models.CharField(max_length=255, null=True, blank=True, verbose_name='家乡')

    def __str__(self):
        return self.telephone

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
