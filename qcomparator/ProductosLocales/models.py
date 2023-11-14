from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Local(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, null=True)
    descripcion = models.TextField(default="")
    # Otros campos relacionados a los locales

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True) # Establece la relación con el modelo Local
    imagen = models.ImageField(upload_to='media/', null=True, blank=True)  # 'upload_to' especifica la carpeta donde se guardarán las imágenes
    tags = models.ManyToManyField('Tag', related_name='productos', blank=True)
    
    def nombre_local(self):
        return self.local.nombre
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Vincula la revisión a un usuario
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Vincula la revisión a un producto
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.user.username} para {self.producto.nombre}"

    
class Tag(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class EditProducto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Vincula la revisión a un usuario
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Vincula la revisión a un producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    
class DeleteProducto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Vincula la revisión a un usuario
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Vincula la revisión a un producto