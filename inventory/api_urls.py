from django.urls import path

from .views import InventoryDetailAPI, InventoryListCreateAPI


urlpatterns = [
    path('', InventoryListCreateAPI.as_view(), name='api_inventory_list'),
    path('<int:pk>/', InventoryDetailAPI.as_view(), name='api_inventory_detail'),
]
