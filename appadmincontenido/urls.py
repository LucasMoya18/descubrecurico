from django.urls import path
from . import views
app_name = 'appadmincontenido'

urlpatterns = [
    path('articulos/', views.articulos, name='articulos'),
    path('articulos/nuevo/<str:tipo>/', views.articulo_crear, name='articulo_crear'),
    path('articulos/<slug:slug>/', views.articulo_detalle, name='articulo_detalle'),
    path('articulos/<slug:slug>/editar/<str:tipo>/', views.articulo_editar, name='articulo_editar'),
    path('articulos/<slug:slug>/eliminar/<str:tipo>/', views.articulo_eliminar, name='articulo_eliminar'),
    path('noticias/<slug:slug>/', views.noticia_detalle, name='noticia_detalle'),
    path('reportajes/<slug:slug>/', views.reportaje_detalle, name='reportaje_detalle'),
    path('eventos/', views.eventos, name='eventos'),
    path('eventos/nuevo/', views.evento_crear, name='evento_crear'),
    path('eventos/<slug:slug>/editar/', views.evento_editar, name='evento_editar'),
    path('eventos/<slug:slug>/eliminar/', views.evento_eliminar, name='evento_eliminar'),
    path('actividades/nuevo/', views.actividad_crear, name='actividad_crear'),
    path('actividades/<slug:slug>/editar/', views.actividad_editar, name='actividad_editar'),
    path('actividades/<slug:slug>/eliminar/', views.actividad_eliminar, name='actividad_eliminar'),

]