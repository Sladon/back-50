from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    # Otros campos relacionados a los productos

class Local(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos relacionados a los locales
