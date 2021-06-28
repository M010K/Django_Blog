from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post-create/', views.post_modify, name='post_create'),
    path('post-update/<int:id>/', views.post_modify, name='post_update'),
    path('post-safe-delete/<int:id>/', views.post_safe_delete, name='post_safe_delete'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
    path('styles.html', views.feature, name='feature'),
]
