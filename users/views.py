from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            # SAVE USER AND STORE IN VARIABLE
            user = form.save()

            # GET STAFF GROUP
            staff_group = Group.objects.get(name='Staff')

            # ASSIGN USER TO STAFF GROUP
            user.groups.add(staff_group)

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})