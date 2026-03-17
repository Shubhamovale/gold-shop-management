from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.inventory_create, name='inventory_add'),
    path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
