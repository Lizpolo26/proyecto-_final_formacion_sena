from django.contrib import admin
from .models import Productos, CarritoItem  # Correcto

# Register your models here.
admin.site.register(Productos)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'descripcion')  # Campos de búsqueda
    list_filter = ('disponible',)  # Filtros
