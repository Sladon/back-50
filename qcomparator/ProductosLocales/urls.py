from django.urls import path, re_path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Define tus rutas aquí
    path('productos/', views.lista_productos, name='lista_productos'),
    path('api/productos/', views.ProductoListAPIView.as_view(), name='producto-list'),
    path('api/locales/', views.LocalListAPIView.as_view(), name='local-list'),
    path('api/productos/crear/', views.CrearProducto.as_view(), name='crear-producto'),
    path('api/productos/<int:pk>/', views.EditarProducto.as_view(), name='producto-detail'),
    path('api/product/<int:product_id>/reviews/', views.ReviewListByProductView.as_view(), name='review-list-by-product'),
    re_path(r'^api/images/(?P<image_path>.*)/$', views.ImageView.as_view(), name='image-view'),
    path('api/reviews/create/', views.CreateReview.as_view(), name='create-review'),
    path('api/locales/<int:pk>/', views.LocalDetailsView.as_view(), name='local-details'),
    path('api/locales/<int:local_id>/productos/', views.ProductosByLocalView.as_view(), name='productos-by-local'),
    path('api/productos/<int:producto_id>/reviews/avg/', views.get_review_avg, name='get_review_avg'),
    path('api/reviews/create/', views.CreateReview.as_view(), name='create-review'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/register/', views.register_view, name='register'),
    path('api/user/<int:user_id>/', views.get_user_details, name='get_user_details'),
    path('api/editproducto/', views.EditProductoCreateView.as_view(), name='editproducto-create'),
    path('api/productos/<int:producto_id>/verificar-ediciones/', views.VerificarEdiciones.as_view(), name='verificar-ediciones'),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    # path('api/producto/', views.ProductoListView.as_view(), name='producto-list'), # Ruta para obtener todos los productos pero pensado para edit productos
]
