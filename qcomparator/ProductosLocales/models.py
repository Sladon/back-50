from django.db import models

class Local(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, null=True)
    descripcion = models.TextField(default="")
    # Otros campos relacionados a los locales

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True) # Establece la relación con el modelo Local
    
    def nombre_local(self):
        return self.local.nombre
    
