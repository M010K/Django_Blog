from django import template
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
        'comment_form' : comment_form,
    }
