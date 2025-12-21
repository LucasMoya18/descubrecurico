from django.urls import path
from . import views

app_name = 'applogin'

urlpatterns = [
    path('login/', views.iniciar, name='iniciar'),
    path('registro/',views.registro, name='registro'),
    path('home/', views.home, name='home'),
    path('salir/',views.salir, name='salir'),
    path('socios/', views.lista_socios_admin, name='lista_socios_admin'),
    path('socios/<int:socio_id>/', views.detalle_socio_admin, name='detalle_socio_admin'),
]
