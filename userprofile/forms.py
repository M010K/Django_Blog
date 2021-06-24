from django import forms

from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    """
    form for user login
    """
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    repeat_password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']

    # 对两次输入的密码是否一致进行检查
    def clean_repeat_password(self):
        data = self.cleaned_data
        if data.get("password") == data.get("repeat_password"):
            return data.get("password")
        else:
            raise forms.ValidationError("两次密码输入不一致,请重试!")

