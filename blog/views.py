import re

import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension, slugify

from .forms import PostForm
from .models import Category, Tag, Post


# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().order_by('-created_time')
        context['category_list'] = Category.objects.all().order_by('-id')
        return context


@login_required(login_url='/userprofile/login')
def blog_index(request, author_id=None):
    if author_id:
        post_list = Post.objects.filter(author_id=author_id)
    else:
        post_list = Post.objects.all().order_by('-created_time')

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')

    post_list = paginator.get_page(page)

    return render(request, 'blog/blog.html', context={"post_list": post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Tag
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        temp_tags = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return Post.objects.filter(tags=temp_tags)


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，需要将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),

            'pymdownx.arithmatex',  # 使用Mathjax渲染网页
        ])
        post.body = md.convert(post.body)

        # 判断是否有目录结构
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


@login_required(login_url='/userprofile/login')
def post_modify(request, id=None):
    # 判断用户是否请求提交数据
    if request.method == "POST":
        post_form = PostForm(data=request.POST)

        # 判断用户提交的数据是否合法
        if post_form.is_valid():
            # 判断是更新还是新建文章
            if id:
                post = Post.objects.get(id=id)
                if request.user != post.author:
                    return HttpResponse("抱歉!你不是本文的作者，无权修改本文!")
                post.title = request.POST['title']
                post.body = request.POST['body']
            else:
                post = post_form.save(commit=False)
                post.author = request.user

            if request.POST['category'] != 'none':
                post.category = Category.objects.get(id=request.POST['category'])
            else:
                post.category = None

            post.save()

            return redirect("blog:index")  # 发布完成后返回到Home页面
        # 用户请求获取数据
    else:
        post_form = PostForm()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        context = {
            "post": Post.objects.get(id=id) if id else None,
            "post_form": post_form,
            "categories": categories,
            "tags": tags
        }

        if id:
            return render(request, 'blog/post_update.html', context=context)
        else:
            return render(request, 'blog/post.html', context=context)


@login_required(login_url='/userprofile/login')
def post_safe_delete(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        if request.user != post.author:
            return HttpResponse("抱歉!你不是本文的作者，无权删除本文!")
        post.delete()
        return redirect('blog:index')
    else:
        return HttpResponse("删除文章仅允许Post请求!")


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def feature(request):
    return render(request, 'blog/styles.html')


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
