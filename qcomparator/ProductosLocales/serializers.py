from rest_framework import serializers
from .models import Producto, Local, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):
    # Agregar un campo solo de lectura para mostrar el nombre del local
    nombre_local = serializers.ReadOnlyField(source='local.nombre')
    imagen = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=False, required=False)
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'nombre_local','imagen')  # Incluye 'nombre_local' en los campos a serializar

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'  # Incluir todos los campos del modelo