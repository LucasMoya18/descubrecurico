from django.urls import path
from . import views

app_name = 'applogin'

urlpatterns = [
    path('login/', views.iniciar, name='iniciar'),
    path('registro/',views.registro, name='registro'),
    path('home/', views.home, name='home'),
    path('salir/',views.salir, name='salir'),

]
