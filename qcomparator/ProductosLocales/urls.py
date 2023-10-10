from django.urls import path
from . import views

urlpatterns = [
    # Define tus rutas aquí
    path('productos/', views.lista_productos, name='lista_productos')
]
