from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Comment(MPTTModel):
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created_time']

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body[:20]
