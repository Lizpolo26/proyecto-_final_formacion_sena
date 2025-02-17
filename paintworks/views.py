from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.

def base (request):
    return render(request,'base.html')

def index (request):
    return render(request,'index.html')

def nosotros (request):
    return render(request, 'nosotros.html')

def contactanos (request):
    return render(request, 'contactanos.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "¡Registro exitoso! Has iniciado sesión.")
                return redirect('ingreso')  # Redirige a la página principal o dashboard

    return render(request, 'registro.html')

def ingreso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Por favor, ingresa ambos campos.')
            return render(request, 'ingreso.html')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
            return render(request, 'ingreso.html')

        if user is not None:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return redirect('/admin/')
            else:
                messages.error(request, "Contraseña incorrecta.")
        else:
            messages.error(request, "El usuario no está registrado.")

    return render(request, 'ingreso.html')

    