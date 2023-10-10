from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Local
from rest_framework import generics
from .serializers import ProductoSerializer, LocalSerializer

class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class LocalListAPIView(generics.ListAPIView):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

def lista_productos(request):
    # Obtener todos los productos (por ahora, productos falsos)
    productos = Producto.objects.all()
    
    # Crear una lista de diccionarios con los datos de los productos
    productos_data = [{"nombre": producto.nombre, "descripcion": producto.descripcion, "precio": producto.precio, "local": producto.local.nombre} for producto in productos]

    # Devolver los datos en formato JSON
    return JsonResponse({"productos": productos_data}, safe=False)