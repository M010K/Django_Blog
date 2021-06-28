from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    博客文章对应的表单类
    """

    class Meta:
        model = Post
        fields = ['title', 'body']  # 定义表单包含的字段
