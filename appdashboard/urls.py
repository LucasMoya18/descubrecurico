from django.urls import path
from . import views

app_name = 'appdashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('socios/', views.lista_socios, name='lista_socios'),
    path('socios/<int:socio_id>/', views.detalle_socio, name='detalle_socio'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/<int:empresa_id>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    path('empresas/', views.lista_empresas_admin, name='lista_empresas_admin'),
    path('empresas/eliminar/<int:empresa_id>/', views.eliminar_empresa_admin, name='eliminar_empresa_admin'),
]
