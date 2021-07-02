from django import template
from django.db.models.aggregates import Count

from django.db.models import Sum
from ..models import Post, Category, Tag
from django.db.models.functions import ExtractYear, ExtractMonth
register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list' : Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time')) \
.values('year', 'month').order_by('year', 'month').annotate(num_posts=Count('id')).filter(num_posts__gt=0)
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    """
    返回所有分类列表
    """
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    """
    返回所有标签列表
    """
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }

@register.inclusion_tag('blog/inclusions/_index_categories.html', takes_context=True)
def show_index_categories(context):
    """
    为主页返回所有分类列表
    """
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }

@register.inclusion_tag('blog/inclusions/_related_tags.html', takes_context=True)
def show_related_tags(context, post):
    """
    返回当前文章post的相关标签列表
    """
    tag_list = Tag.objects.filter(post=post).order_by('id')
    return {
        'tag_list': tag_list,
    }

@register.inclusion_tag('blog/inclusions/_total_views.html', takes_context=True)
def show_total_views(context):
    """
    返回当前所有文章的总阅读量
    """
    view_count = Post.objects.aggregate(nums=Sum('views'))
    return {
        'view_count': view_count,
    }