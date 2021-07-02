from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blog.models import Post
from .models import Comment
from .forms import CommentForm


@login_required(login_url='/userprofile/login/')
def post_comment(request, post_id, parent_comment_id=None):
    # 检查用户是否具有评论权限
    if not request.user.has_perm('comments.add_comment'):
        return HttpResponse("抱歉!你无权发布评论!具体请在主页联系M010K!")

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # return HttpResponse('200 OK')
                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})

            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method == "GET":
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'post_id': post_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comments/reply.html', context)
    # 处理错误请求
    else:
        return HttpResponse("仅接受GET/POST请求。")
