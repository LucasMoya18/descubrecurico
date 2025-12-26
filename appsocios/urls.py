from django.urls import path
from . import views

app_name = 'appsocios'

urlpatterns = [
    path('empresas/', views.empresas, name='empresas'),
    path('registrarsocio/', views.crear_socio, name='crear_socio'),
    path('loginsocio/', views.login_socio, name='login_socio'),
    path('empresa/registro/', views.crear_empresa, name='crear_empresa'),
    path('empresa/editar/<int:id_empresa>/', views.editar_empresa, name='editar_empresa'),
    path('rubros/', views.lista_rubros, name='lista_rubros'),
    path('rubros/crear/', views.crear_rubro, name='crear_rubro'),
    path('rubros/editar/<int:id_rubro>/', views.editar_rubro, name='editar_rubro'),
    path('rubros/eliminar/<int:id_rubro>/', views.eliminar_rubro, name='eliminar_rubro'),
    path('tipos-comercializacion/', views.lista_tipos_comercializacion, name='lista_tipos_comercializacion'),
    path('tipos-comercializacion/crear/', views.crear_tipo_comercializacion, name='crear_tipo_comercializacion'),
    path('tipos-comercializacion/editar/<int:id_tipo>/', views.editar_tipo_comercializacion, name='editar_tipo_comercializacion'),
    path('tipos-comercializacion/eliminar/<int:id_tipo>/', views.eliminar_tipo_comercializacion, name='eliminar_tipo_comercializacion'),
    path('encuesta/', views.encuesta, name='encuesta'),
    path('encuesta/continuar/<int:id_empresa>/', views.continuar_encuesta, name='continuar_encuesta'),
    path('lista-empresas/', views.lista_empresas, name='lista_empresas'),
    path('editar-perfil/', views.editar_socio, name='editar_socio'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
]