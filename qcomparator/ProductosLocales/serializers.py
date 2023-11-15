from rest_framework import serializers
from .models import Producto, Local, Review, Tag, EditProducto


class EditProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditProducto
        fields = '__all__'

# class ProductoListView(generics.ListAPIView):
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'nombre')  # Incluye 'nombre' en los campos a serializar

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

        
class ProductoSerializer(serializers.ModelSerializer):
    # Agregar un campo solo de lectura para mostrar el nombre del local
    nombre_local = serializers.ReadOnlyField(source='local.nombre')
    imagen = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=False, required=False)
    tags = TagSerializer(many=True, read_only=True)  # Usa el serializador de etiquetas
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'nombre_local','imagen','tags')  # Incluye 'nombre_local' en los campos a serializar

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'  # Incluir todos los campos del modelo