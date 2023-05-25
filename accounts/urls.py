from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("get-profile-info/<int:user_id>/", views.get_profile_info, name="get-profile-info"),
   
]