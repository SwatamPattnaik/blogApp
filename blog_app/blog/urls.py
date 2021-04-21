from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('<int:blog_id>/',views.blog_page, name='blog_page'),
    path('blog_form/', views.blog_form, name='blog_form'),
    path('edit_blog/<int:blog_id>', views.edit_blog, name='edit_blog'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('approve_comment/', views.approve_comment, name='approve_comment'),
    path('reject_comment/', views.reject_comment, name='reject_comment')
]