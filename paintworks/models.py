from django.db import models
from django.contrib.auth.models import User

class servicios(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
# Create your models here.
class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    servicios = models.ForeignKey(servicios, on_delete=models.CASCADE)  # Referencia al modelo Servicios
    cantidad = models.IntegerField(default=1)

    def subtotal(self):
        return self.servicios.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.servicios.nombre}"

    
class Orden(models.Model): 
     usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, 
     blank=True) 
     nombre = models.CharField(max_length=200) 
     email = models.EmailField() 
     telefono = models.CharField(max_length=20) 
     sesion_id = models.CharField(max_length=100, null=True, blank=True) 
     total = models.DecimalField(max_digits=10, decimal_places=0) 
     metodo_pago = models.CharField(max_length=20, choices=[('nequi', 'Nequi'), ('bancolombia', 'Bancolombia')]) 
     pagado = models.BooleanField(default=False) 
     fecha_creacion = models.DateTimeField(auto_now_add=True) 
      
     def __str__(self): 
         return f"Orden #{self.id} - {self.nombre}" 
  
class OrdenItem(models.Model): 
     orden = models.ForeignKey(Orden, related_name='items', 
     on_delete=models.CASCADE) 
     servicios = models.ForeignKey(servicios, on_delete=models.CASCADE) 
     precio = models.DecimalField(max_digits=10, decimal_places=0) 
     cantidad = models.IntegerField(default=1) 
      
     def __str__(self): 
         return f"{self.cantidad} x {self.servicios.nombre}" 
      
     def subtotal(self): 
         return self.precio * self.cantidad 


