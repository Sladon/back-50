from rest_framework import serializers
from .models import Producto, Local

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'  # Esto serializa todos los campos del modelo


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'  # Incluir todos los campos del modelo