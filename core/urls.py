from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-image/', views.upload_image, name='upload-image'),
    path('get-images/', views.get_images, name='get-images'),
    path('get-images/<int:user_id>/', views.get_images_by_user_id, name='get-images-by-user-id'),
]