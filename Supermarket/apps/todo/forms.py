from django import forms
from django.core import validators
from django.forms import Form

from todo.helper import set_password
from todo.models import User


class RegForm(forms.ModelForm):
    # 注册的表单验证
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必须填',
                                    'max_length': '密码最大长度为16位',
                                    'min_length': '密码最小长度为6位',
                                }

                                )  # 密码大小写字母数字组成,6到16位

    password2 = forms.CharField(error_messages={'required': '确认密码必填', })

    class Meta:
        model = User
        # 需要验证的字段
        fields = ['telephone', ]

        error_messages = {
            "telephone": {
                "required": "手机号码必填"
            }
        }



    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        ee = User.objects.filter(telephone=telephone).exists()
        if ee:
            raise forms.ValidationError('手机号码已经存在')
        return telephone

    def clean_password2(self):
        #验证两个密码是否一致
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError('密码输入不一致')
        return pwd2


class LoginForm(forms.ModelForm):
    """登陆的form表单"""
    class Meta:
        model = User
        fields = ['telephone', 'password']

        error_messages = {
            'telephone': {
                "required": "手机号码必填"
            },
            'password': {
                "required": "密码必填"
            }
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        # 获取用手机和密码
        telephone = cleaned_data.get('telephone')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([telephone, password]):
            # 根据手机号码获取用户
            try:
                user1 = User.objects.get(telephone=telephone)
            except User.DoesNotExist:
                raise forms.ValidationError({"telephone": "该用户不存在!"})

            # 判断密码
            if user1.password != set_password(password):
                raise forms.ValidationError({"password": "密码填写错误!"})

            # 将用户信息保存
            cleaned_data['user1'] = user1
            return cleaned_data
        else:
            return cleaned_data




