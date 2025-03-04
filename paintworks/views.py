from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout   
from smtplib import SMTPException
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from Proyecto_SENA import settings

# Create your views here.

def base (request):
    return render(request,'base.html')

def index (request):
    return render(request,'index.html')

def servicios (request):
    return render(request,'servicios.html')

def nosotros (request):
    return render(request, 'nosotros.html')

def contactanos (request):
    return render(request, 'contactanos.html')

def perfil (request):
    return render(request, 'perfil.html')


def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('registro')

        if User.objects.filter(username=nombre).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return redirect('registro')

        if User.objects.filter(email=correo).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return redirect('registro')

        user = User.objects.create_user(username=nombre, email=correo, password=password)
        user.save()
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('ingreso')

    return render(request, 'registro.html')


def ingreso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        password = request.POST['password']

        user = authenticate(request, username=nombre, password=password)
        if user is not None:
            # Iniciar sesión
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('index')  # Redirigir a la página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return redirect('ingreso')

    return render(request, 'ingreso.html')

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/cambiar_contrasena/{uid}/{token}/")
            send_mail(
                'Restablecer contraseña',
                f'Haz clic en el siguiente en enlace para restablecer tu contraseña {enlace}',
                'lizreina0126@gmail.com',
                [email], 
                fail_silently=False
            )
            messages.success(request, "Se ah enviado un enlace de restablecimiento de contraseña a su correo")
            return redirect('registro')
        else:
            messages.success(request, "No se encontro algun usuario registrado con ese correo")
        return redirect('restablecer')
    return render(request, 'email_restablecer.html')

def cambiar_contrasena(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST.get("password")
            
            if not nueva_contrasena:
                messages.error(request, "La contraseña no puede estar vacía")
                return render(request, "email_contrasena.html")
                
            
            user.set_password(nueva_contrasena)
            user.save()
            
            return redirect('confirmacion_contrasena')
        
        return render(request, "email_contrasena.html")
    return redirect("registro")

def confirmacion_contrasena(request):
    return render(request, "cambio_contrasena.html")



def enviar_correo(request):
    if request.method == 'POST':
        print(request)# Obtener datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Construir contenido del correo
        contenido = (
            f"Nombre: {nombre}\n"
            f"Teléfono: {telefono}\n"
            f"Correo: {correo}\n"
            f"Asunto: {asunto}\n"
            f"Mensaje: {mensaje}"
        )

        try:
            # Enviar correo usando send_mail de Django
            send_mail(
                'Nuevo mensaje de contacto',  # Asunto del correo
                contenido,  # Cuerpo del correo
                'lizreina0126@gmail.com',  # Remitente (debe coincidir con EMAIL_HOST_USER)
                ['lizreina0126@gmail.com'],  # Lista de destinatarios
                fail_silently=False,  # Si es True, no se mostrarán errores
            )

            # Mensaje de éxito
            messages.success(request, "Mensaje enviado correctamente.")
        
        except Exception as e:
            # Mensaje de error
            messages.error(request, "Error al enviar el mensaje. Inténtalo de nuevo más tarde.")
            print(e)  # Loguear el error (opcional)

    # Renderizar la plantilla con los mensajes
    return render(request, 'contactanos.html')

def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')  # Redirige a la página de inicio


@login_required  # Asegura que solo usuarios autenticados puedan acceder
def perfil(request):
    return render(request, 'perfil.html', {'user': request.user})

