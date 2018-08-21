from django import forms
from django.core.validators import ValidationError,RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用戶名",
        min_length=4,
        error_messages={
            "required":"用户名不能为空！",
            "min_length":"用户名不能少于4位！",
        },
        widget=forms.widgets.TextInput(
            attrs={"class":"form-control","placeholder":'请输入用户名',"autocomplete":"off"}
        )
    )
    password = forms.CharField(
        label="密碼",
        min_length=4,
        error_messages={
            "required": "密码不能为空！",
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control","placeholder":'请输入密码',"autocomplete":"off"},
            render_value=True
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        min_length=6,
        max_length=12,
        label="用户名",
        error_messages={
            "min_length": "用户名不能少于6位！",
            'required': "用户名不能为空！"
        },
        widget=forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入用户名"
            }
        )
    )
    password = forms.CharField(
        label="密码",
        error_messages={
            "required": "密码不能为空！",
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control', "placeholder": "请输入密码"},
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )
    rep_password = forms.CharField(
        label="确认密码",
        error_messages={
            "required": "确认密码不能为空！",
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control', "placeholder": "请输入密码"},
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )
    phone = forms.CharField(
        # disabled=True,
        label="手机",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机格式不正确！"), ],
        error_messages={
            "required": "电话号码不能为空！",
        },
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control', "placeholder": "请输入电话号码"},
        )
    )
    email = forms.CharField(
        # disabled=True,
        label="邮箱",
        validators=[RegexValidator(r'^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$', "邮箱格式不正确！"), ],
        error_messages={
            "required": "邮箱不能为空！",
        },
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control', "placeholder": "请输入邮箱"},
        )
    )


    def clean(self):
        password = self.cleaned_data.get("password")
        rep_password = self.cleaned_data.get("rep_password")

        if password == rep_password:
            return self.cleaned_data
        else:
            self.add_error("rep_password","两次密码不一致！")
            raise ValidationError("两次密码不一致！")

