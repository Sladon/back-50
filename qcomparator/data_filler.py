import random
from django.db import models
from faker import Faker
import os
import django
import csv

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcomparator.settings")

# Inicializar Django
django.setup()

# Ahora puedes importar tus modelos
from ProductosLocales.models import Local, Producto, Review, Tag
from django.contrib.auth.models import User  # Importa el modelo User

def create_fake_users(num_users=10):
    fake = Faker()
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()  # O puedes usar una contraseña fija
        user = User.objects.create_user(username=username, email=email, password=password)

# Función para rellenar la base de datos con datos falsos
def fill_database_with_fake_data():

    # Create Locations
    with open('./Locales.csv', 'r', newline = '') as csvfile:

        for line in csvfile.readlines():
            data = line.strip().split(',')

            nombre_local = data[0]
            ubicacion_local = data[1]
            descripcion_local = data[2]
            local = Local(nombre=nombre_local, ubicacion=ubicacion_local, descripcion=descripcion_local)
            local.save()
    

    # Create Products
    with open('./Productos.csv', 'r', newline = '') as csvfile:

        for line in csvfile.readlines():
            data = line.strip().split(',')

            nombre_producto = data[0]
            descripcion_producto = data[1]
            precio_producto = float(data[2])
            local_id = int(data[3])
            local = Local.objects.get(id = local_id)
            image = "media/" + data[4]
            producto = Producto(nombre=nombre_producto, descripcion=descripcion_producto, precio=precio_producto, local=local, imagen=image)
            producto.save()

            tags = data[5].split(";")
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(nombre=tag_name) # If tag is found, then its returned. Else, it creates a new tag and returns the new created one
                producto.tags.add(tag)

            producto.save()

if __name__ == "__main__":
    create_fake_users()
    fill_database_with_fake_data()
    print("ready faker")

