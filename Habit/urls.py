from django.urls import path 
from .import views

urlpatterns = [
    path('add_task/', views.addtask, name='addtask'),
    path('toggle_today/<int:pk>/', views.toggle_today, name='toggle_today'),
    path('mark_delete/<int:pk>/', views.mark_delete, name='mark_delete'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
]