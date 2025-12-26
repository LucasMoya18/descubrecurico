from django.urls import path
from . import views

app_name = 'appdashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('socios/', views.lista_socios, name='lista_socios'),
    path('socios/<int:socio_id>/', views.detalle_socio, name='detalle_socio'),
]
