from django import template
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post, user):
    comment_list = post.comments.all().order_by('-created_time')
    comment_form = CommentForm()
    return {
        'post': post,
        'user': user,
        'comments_list': comment_list,
        'comment_form': comment_form,
    }


@register.inclusion_tag('comments/inclusions/_total_comments.html', takes_context=True)
def show_total_comments(context):
    comment_count = Comment.objects.all().count()
    return {
        'comment_count': comment_count
    }
