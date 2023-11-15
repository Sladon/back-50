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

from ProductosLocales.models import Local, Producto, Review, Tag, CustomUser

    

def create_fake_users(num_users=10):
    fake = Faker()
    users = []

    # Admin user
    username = "roberto"
    email = "roberto@miuandes.cl"
    password = "hola123"
    rol = "admin"
    user = CustomUser(username=username, email=email, rol=rol)
    user.set_password(password)
    users.append(user)

    # Other users
    for i in range(2, 10):
        username = f"roberto{i}"
        email = f"roberto{i}@miuandes.cl"
        password = "hola123"
        rol = "client"
        user = CustomUser(username=username, email=email, rol=rol)
        user.set_password(password)
        users.append(user)

    # Fake users
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = "hola123"
        rol = "client"
        
        # Ensure unique email addresses
        while CustomUser.objects.filter(email=email).exists():
            email = fake.email()

        user = CustomUser(username=username, email=email, rol=rol)
        user.set_password(password)
        users.append(user)

    CustomUser.objects.bulk_create(users)

def create_fake_reviews(num_reviews=50):
    fake = Faker()
    reviews = []
    for _ in range(num_reviews):
        rand_user = random.randint(1, 10)
        rand_product_id = random.randint(1, Producto.objects.count())
        ran_sentence = random.randint(1, 3)
        rand_rating = random.randint(0, 5)

        user = CustomUser.objects.get(id=rand_user)
        producto = Producto.objects.get(id=rand_product_id)
        comentario = fake.paragraph(nb_sentences=ran_sentence, variable_nb_sentences=True)
        rating = rand_rating

        review = Review(user=user, producto=producto, comentario=comentario, calificacion=rating)
        reviews.append(review)  

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
    create_fake_reviews()
    print("ready faker")

