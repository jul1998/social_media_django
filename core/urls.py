from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-image/', views.upload_image, name='upload-image'),
    path('get-images/', views.get_images, name='get-images'),
    path('get-images/<int:user_id>/', views.get_images_by_user_id, name='get-images-by-user-id'),
    path('get-comments/<int:image_id>/', views.get_comments_by_image, name='get-comments'),
   path('post-comment/', views.post_comment, name='post-comment'),
]