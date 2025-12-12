from django.urls import path
from . import views

app_name = 'appsocios'

urlpatterns = [
    path('empresas/', views.empresas, name='empresas'),
    path('registrarsocio/', views.crear_socio, name='crear_socio'),
    path('empresa/registro/', views.crear_empresa, name='crear_empresa'),
    path('empresa/editar/<int:id_empresa>/', views.editar_empresa, name='editar_empresa'),
    path('crear-rubro/', views.crear_rubro, name='crear_rubro'),
    path('crear-tipo-comercializacion/', views.crear_tipo_comercializacion, name='crear_tipo_comercializacion'),
    path('encuesta/', views.encuesta, name='encuesta'),
    path('lista-empresas/', views.lista_empresas, name='lista_empresas'),
]