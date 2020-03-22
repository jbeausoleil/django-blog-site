from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('blog.urls')),
    re_path(r'accounts/login/$', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path(r'accounts/logout/$', views.LogoutView.as_view(), name='logout')
]