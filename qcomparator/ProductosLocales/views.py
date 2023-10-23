from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Local
from rest_framework import generics
from .serializers import ProductoSerializer, LocalSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CrearProducto(APIView):
    def post(self, request, format=None):
        # Serializa los datos recibidos en la solicitud
        serializer = ProductoSerializer(data=request.data)

        if serializer.is_valid():
            # Guarda el objeto serializado en la base de datos
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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


# @api_view(['GET', 'POST'])
# def lista_productos(request):
#     if request.method == 'GET':
#         # Obtener todos los productos
#         productos = Producto.objects.all()
#         serializer = ProductoSerializer(productos, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # Crear un nuevo producto
#         serializer = ProductoSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)