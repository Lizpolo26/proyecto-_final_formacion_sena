"""
URL configuration for Proyecto_SENA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paintworks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='base'),
    path('index/', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contactanos/', views.contactanos, name='contactanos'),  # Página de contacto
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),  # Nueva URL para enviar el correo
    path('ingreso/', views.ingreso, name='ingreso'),
    path('registro/', views.registro, name='registro'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path('cambiar_contrasena/<uidb64>/<token>/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('confirmacion_contrasena/', views.confirmacion_contrasena, name='confirmacion_contrasena'),            
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.cerrar_sesion, name='logout'),
]


