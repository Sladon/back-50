from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from django.http import JsonResponse
from .models import Producto, Local, Review, Tag, CustomUser, EditProducto
from .serializers import ProductoSerializer, LocalSerializer, ReviewSerializer, EditProductoSerializer, ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse
from django.views import View
import os
from django.db.models import Avg
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


class VerificarEdiciones(APIView):
    def get(self, request, producto_id):
        # Obtener el producto o devolver 404 si no existe
        producto = get_object_or_404(Producto, pk=producto_id)

        # Verificar si hay solicitudes de edición para este producto
        tiene_ediciones = EditProducto.objects.filter(producto=producto_id).exists()

        # Serializar el producto
        serializer = ProductoSerializer(producto)

        # Devolver una respuesta indicando si tiene o no solicitudes de edición
        response_data = {
            'producto': serializer.data,
            'tiene_ediciones': tiene_ediciones,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class EditProductoCreateView(generics.CreateAPIView):
    queryset = EditProducto.objects.all()
    serializer_class = EditProductoSerializer

    def perform_create(self, serializer):
        # Llama al método save personalizado del modelo para manejar la lógica de actualización del producto
        instance = serializer.save()
        instance.save_product_price()

        return instance

# class ProductoListView(generics.ListAPIView): # Ruta para obtener todos los productos pero pensado para edit productos
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer


def get_user_details(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'rol': user.rol,
            # Agrega más campos según tus necesidades
        }
        return JsonResponse({'user': user_data})
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data['username']
#         password = data['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             # Devolver todos los datos del usuario
#             user_data = {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'rol': user.rol,
#                 # Agrega más campos según tus necesidades
#             }
#             return JsonResponse({'user': user_data})
#         else:
#             return JsonResponse({'message': 'Invalid credentials'}, status=401)
        

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': user.rol,
                # Agrega más campos según tus necesidades
            }

            return JsonResponse({'user': user_data})
        else:
            # Devuelve mensajes de error específicos en la respuesta JSON
            errors = {'non_field_errors': ['Invalid credentials']}
            return JsonResponse({'message': 'Invalid credentials', 'errors': errors}, status=401)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = CustomUserCreationForm(data)

        if form.is_valid():
            user = form.save()
            return JsonResponse({'message': 'Registration successful'})
        else:
            # Imprime los errores en la consola de Django
            print(form.errors)
            
            # Devuelve mensajes de error específicos en la respuesta JSON
            errors = dict(form.errors.items())
            return JsonResponse({'message': 'Invalid registration data', 'errors': errors}, status=400)


class CreateReview(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@api_view(['GET']) 
def get_review_avg(request, producto_id):

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    
    avg_rating = Review.objects.filter(producto=producto).aggregate(avg_rating=Avg('calificacion'))
    avg = avg_rating['avg_rating']
    count = Review.objects.filter(producto=producto).count()

    return Response({'producto': producto.nombre, 'avg_rating': avg, 'count': count})


class ProductosByLocalView(ListAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        local_id = self.kwargs.get('local_id')
        local = get_object_or_404(Local, pk=local_id)
        return Producto.objects.filter(local=local)

class ImageView(View):
    def get(self, request, image_path):
        # Construir la ruta completa a la imagen
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # Verificar si la imagen existe
        if os.path.exists(full_image_path):
            # Abrir la imagen y devolver su contenido
            with open(full_image_path, 'rb') as image_file:
                return HttpResponse(image_file.read(), content_type="image/jpeg")
        else:
            # Si la imagen no existe, devolver una respuesta 404
            return HttpResponse("La imagen no existe", status=404)


class ReviewListByProductView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(producto_id=product_id)

class EditarProducto(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

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


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class LocalDetailsView(RetrieveAPIView):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene la instancia del local
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
