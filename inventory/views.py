from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum, Count
from .models import Inventory
from .forms import InventoryForm
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import InventorySerializer

class InventoryListCreateAPI(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]


class InventoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    
@login_required
@permission_required('inventory.view_inventory', raise_exception=True)
def inventory_list(request):
    items = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})


@login_required
@permission_required('inventory.add_inventory', raise_exception=True)
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user
            inventory.save() 
            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'inventory/inventory_form.html', {'form': form})


@login_required
@permission_required('inventory.change_inventory', raise_exception=True)
def inventory_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)

    return render(request, 'inventory/inventory_form.html', {'form': form})

@login_required
@permission_required('inventory.delete_inventory', raise_exception=True)
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')

    return render(request, 'inventory/inventory_confirm_delete.html', {'item': item})

@login_required
@permission_required('inventory.view_inventory', raise_exception=True)
def dashboard(request):
    total_items = Inventory.objects.count()
    total_quantity = Inventory.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    low_stock_items = Inventory.objects.filter(quantity__lte=5)

    context = {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'low_stock': low_stock_items,
    }
    return render(request, 'dashboard.html', context)