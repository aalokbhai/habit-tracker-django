from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.about_page, name='about'),
    path('home/', views.home, name='home'),
    path('Habit/', include('Habit.urls')),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Custom logout view
    path('signup/', views.signup, name='signup'),
]