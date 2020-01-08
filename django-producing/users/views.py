from django.shortcuts import render, redirect
from .tasks import generate_and_send_token
from .forms import RegisterForm


def index(request):
    return render(request, 'users/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            generate_and_send_token.delay(username)
            return redirect('auth')
    else:
        form = RegisterForm()
    return render(request, 'users/registration.html', {'form': form})

