from django.urls import path, re_path
from . import views

urlpatterns = [
    # Define tus rutas aquí
    path('productos/', views.lista_productos, name='lista_productos'),
    path('api/productos/', views.ProductoListAPIView.as_view(), name='producto-list'),
    path('api/locales/', views.LocalListAPIView.as_view(), name='local-list'),
    path('api/productos/crear/', views.CrearProducto.as_view(), name='crear-producto'),
    path('api/productos/<int:pk>/', views.EditarProducto.as_view(), name='producto-detail'),
    path('api/reviews/product/<int:product_id>/', views.ReviewListByProductView.as_view(), name='review-list-by-product'),
    re_path(r'^api/images/(?P<image_path>.*)/$', views.ImageView.as_view(), name='image-view'),
    path('api/reviews/create/', views.CreateReview.as_view(), name='create-review'),
]
