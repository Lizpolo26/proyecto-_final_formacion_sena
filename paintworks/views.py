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


from django.core.mail import send_mail 
from django.shortcuts import render, redirect 
from django.contrib import messages 
from .models import Orden, OrdenItem, CarritoItem
from .forms import OrdenForm 
 

#vista de pasarela de compras

from .models import Datos, CarritoItem, OrdenItem
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import OrdenForm

def pasarela(request):
    carrito_items = []
    total = 0

    # Obtener los productos del carrito según el usuario o sesión
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)

    # Si el carrito está vacío, mostrar advertencia
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')

    # Calcular el total del pedido
    for item in carrito_items:
        total += item.subtotal()

    if request.method == 'POST':
        form = OrdenForm(request.POST)
        metodo_pago = request.POST.get('metodo_pago')

        if form.is_valid() and metodo_pago:
            orden = form.save(commit=False)

            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key

            orden.total = total
            orden.metodo_pago = metodo_pago
            orden.save()

            # Guardar los productos en la orden
            for item in carrito_items:
                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    precio=item.producto.precio,
                    cantidad=item.cantidad
                )

            # Vaciar el carrito después del pago
            carrito_items.delete()

            # 📧 Enviar el correo de confirmación
            enviar_correo_confirmacion(orden)

            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmar', orden_id=orden.id)
        else:
            messages.error(request, "Por favor selecciona un método de pago válido.")
    else:
        # Precargar los datos del usuario en el formulario
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos_usuario = Datos.objects.get(usuario=request.user)
                initial_data = {
                    'nombre': f"{datos_usuario.nombre} {datos_usuario.apellido}",
                    'email': request.user.email
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email
                }

        form = OrdenForm(initial=initial_data)

    return render(request, 'pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })


def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        else:
            orden = Orden.objects.get(id=orden_id, sesion_id=request.session.session_key)

        items = OrdenItem.objects.filter(orden=orden)

        return render(request, 'confirmacion.html', {
            'orden': orden,
            'items': items
        })

    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('productos')


def enviar_correo_confirmacion(orden):
    """ Envía un correo de confirmación al cliente """
    asunto = f"Confirmación de Pedido #{orden.id}"
    mensaje = f"""
    Hola {orden.nombre},

    Gracias por tu compra. Hemos recibido tu pedido y estamos verificando el pago.

    🛍 *Detalles del Pedido*
    - Número de Pedido: {orden.id}
    - Total: ${orden.total}
    - Método de Pago: {orden.get_metodo_pago_display()}
    - Fecha: {orden.fecha_creacion.strftime('%d/%m/%Y %H:%M')}

    📦 *Productos Comprados*:
    """



#carrito

from .models import Productos, CarritoItem  

def productos(request):
    producto_lista = Productos.objects.all()

    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id')
        try:
            producto = Productos.objects.get(id=producto_id)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto_id,
                    sesion_id=sesion_id,
                    usuario=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Productos.DoesNotExist:
            messages.error(request, "Producto no encontrado")
    
    return render(request, 'productos.html', {'productos': producto_lista})

def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    for item in carrito_items:
        total += item.subtotal()
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Servicio eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Servicio no encontrado")
        
    return redirect('ver_carrito')


