from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.role = 'staff'
            user.save(update_fields=['role'])

            # GET OR CREATE STAFF GROUP (won't crash if missing)
            staff_group, created = Group.objects.get_or_create(name='Staff')

            user.groups.add(staff_group)

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
