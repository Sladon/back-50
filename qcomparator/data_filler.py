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
from ProductosLocales.models import Local, Producto



# Función para rellenar la base de datos con datos falsos
def fill_database_with_fake_data(num_locales=10, num_productos_por_local=5):
    fake = Faker()

    # Rellena la tabla Local
    for _ in range(num_locales):
        nombre_local = fake.company()
        ubicacion_local = fake.address()
        local = Local(nombre=nombre_local, ubicacion=ubicacion_local)
        local.save()

        # Rellena la tabla Producto para cada Local
        for _ in range(num_productos_por_local):
            nombre_producto = fake.word()
            descripcion_producto = fake.text()
            precio_producto = round(random.uniform(1, 100), 2)  # Precio aleatorio entre 1 y 100
            producto = Producto(nombre=nombre_producto, descripcion=descripcion_producto, precio=precio_producto, local=local)
            producto.save()
    print("ready faker")

if __name__ == "__main__":
    fill_database_with_fake_data()
