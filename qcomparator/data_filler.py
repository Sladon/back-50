import random
from django.db import models
from faker import Faker
import os
import django

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
def fill_database_with_fake_data(num_locales=10, num_productos_por_local=5, num_reviews_per_product=10):
    fake = Faker()

    # Lista de etiquetas ficticias
    fake_tags = ['Dulce', 'Salado', 'Picante', 'Vegetariano', 'Orgánico', 'Sin gluten']

    # Rellena la tabla Local
    for _ in range(num_locales):
        nombre_local = fake.company()
        ubicacion_local = fake.address()
        descripcion_local = fake.text()
        local = Local(nombre=nombre_local, ubicacion=ubicacion_local, descripcion=descripcion_local)
        local.save()

        # Rellena la tabla Producto para cada Local
        for _ in range(num_productos_por_local):
            nombre_producto = fake.word()
            descripcion_producto = fake.text()
            precio_producto = round(random.uniform(200, 100000), 2)  # Precio aleatorio entre 1 y 100
            producto = Producto(nombre=nombre_producto, descripcion=descripcion_producto, precio=precio_producto, local=local)
            producto.save()

            num_tags = random.randint(1, len(fake_tags))  # Número aleatorio de etiquetas a asignar
            tags = fake.random_elements(elements=fake_tags, length=num_tags, unique=True)
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(nombre=tag_name)
                producto.tags.add(tag)  # Agrega la etiqueta al producto

            producto.save()  # Guarda el producto después de asociar las etiquetas

            # Rellena la tabla Review para cada Producto
            for _ in range(num_reviews_per_product):
                user_id = random.randint(1, 10)  # Suponiendo que tienes 10 usuarios en la base de datos
                comentario_review = fake.paragraph()
                calificacion_review = random.randint(1, 5)  # Calificación aleatoria entre 1 y 5
                review = Review(user_id=user_id, producto=producto, comentario=comentario_review, calificacion=calificacion_review)
                review.save()


if __name__ == "__main__":
    create_fake_users()
    fill_database_with_fake_data()
    print("ready faker")

