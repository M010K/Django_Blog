import markdown
from django.utils.html import strip_tags

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """
    博客的分类模型
    """
    name = models.CharField(max_length=100)
    # 分类摘要
    excerpt = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客的标签模型
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    博客的文章模型
    """

    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文，使用 TextField 来存储大段文本。
    body = models.TextField('正文')

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 文章分类与标签，分类与标签的模型已经定义在上面
    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    author = models.ForeignKey(
        User, verbose_name='作者', on_delete=models.CASCADE)

    # 新增 views 字段记录阅读量
    # editable=False表示不允许通过后台设置这一数据
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        修改文章时更新modified_time
        """
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        返回博客详情页的绝对url
        """
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        """
        将访问次数加一并更新数据库
        """
        self.views += 1
        self.save(update_fields=['views'])
