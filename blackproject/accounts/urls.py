# accounts/urls.py

from django.urls import path
from .  import views

urlpatterns = [
    path('', views.test, name='test'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('face/', views.user_face_check, name='face'),
    path('alldata/', views.alldata, name='t'),
     path('add-stock/', views.add_stock, name='addstock'),
]