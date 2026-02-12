from django.urls import path
from . import views
from .views import InventoryListCreateAPI, InventoryDetailAPI

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.inventory_create, name='inventory_add'),
    path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', InventoryListCreateAPI.as_view(), name='api_inventory_list'),
    path('<int:pk>/', InventoryDetailAPI.as_view(), name='api_inventory_detail'),
]