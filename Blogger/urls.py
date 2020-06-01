"""Blogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Blog.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='home'),
    path('about/',about,name='about'),
    path('login/',Login,name='login'),
    path('contact/',contact,name='contact'),
    path('signup/',signup,name='signup'),
    path('blog/<int:bid>',Blog_detail,name='blog_d'),
    path('blog_like/<int:pid>',Like_post,name='like'),
    path('logout/',Logout,name='logout'),
    path('blog_com/<int:pid>',Post_comment,name='comment'),
    path('myblog/',Myblogs,name='myblog'),
    path('blog_del/<int:bid>',blog_delete,name='blog_del'),
    path('cat_d/<int:cid>',category_detail,name='cat_d'),
    path('add_blog/',add_blog,name='blog_d'),
    path('change_p/',Change_Image,name='change_p'),
    path('changepas/',change_pas,name='changepas')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
