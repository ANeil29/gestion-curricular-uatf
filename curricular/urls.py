from django.urls import path
from . import views

app_name = 'curricular'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('rediseño/<int:rediseño_id>/', views.detalle_rediseño, name='detalle_rediseño'),
    path('fase/<int:seguimiento_id>/actualizar/', views.actualizar_fase, name='actualizar_fase'),
    path('fase/<int:seguimiento_id>/subir-archivo/', views.subir_archivo_ca, name='subir_archivo_ca'),
    path('archivo/<int:archivo_id>/descargar/', views.descargar_archivo_ca, name='descargar_archivo_ca'),
    path('archivo/<int:archivo_id>/eliminar/', views.eliminar_archivo_ca, name='eliminar_archivo_ca'),
    path('reporte/pdf/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]