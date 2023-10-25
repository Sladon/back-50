from django.urls import path
from . import views

urlpatterns = [
    # Define tus rutas aquí
    path('productos/', views.lista_productos, name='lista_productos'),
    path('api/productos/', views.ProductoListAPIView.as_view(), name='producto-list'),
    path('api/locales/', views.LocalListAPIView.as_view(), name='local-list'),
    path('api/productos/crear/', views.CrearProducto.as_view(), name='crear-producto'),
    path('api/productos/<int:pk>/', views.EditarProducto.as_view(), name='producto-detail'),
]
