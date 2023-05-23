from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-image/', views.upload_image, name='upload-image'),
]