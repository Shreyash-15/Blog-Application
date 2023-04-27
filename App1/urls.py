from django.urls import path
from .views import *
from .views import MyPasswordResetView
from django.contrib.auth import views as auth_views
from .views import BlogPostDetailView
from django.urls import path
from . import views


urlpatterns = [
    path('',blogs,name='blogs'),
    path('register/',Register,name='register'),
    path('login/',Login,name='login'),
    path('profile/',Profile,name='profile'),
    path('edit/<int:id>/', edit_view, name='edit_view'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('add_blogs/',add_blogs,name='add_blogs'),
    path('logout/',userlogout,name='logout'),
    path('delete/<int:id>/', delete_view, name='delete_view'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', MyPasswordResetView.as_view(), name='password_reset'),
    # path('logs/', views.log_view, name='logs'),
    path('logs/', logs, name='logs'),
]



