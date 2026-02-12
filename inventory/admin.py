from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'weight_grams', 'price', 'quantity')
    search_fields = ('name',)
    list_filter = ('category',)
