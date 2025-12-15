from django.contrib import admin
from .models import (
    Sede, Facultad, Carrera, Fase, RediseñoCurricular, 
    SeguimientoFase, ArchivoComisionAcademica
)

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono']
    search_fields = ['nombre']

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'facultad', 'sede', 'grado_academico', 'activo']
    list_filter = ['sede', 'facultad', 'grado_academico', 'activo']
    search_fields = ['nombre', 'facultad__nombre']
    list_per_page = 50

@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'codigo', 'orden']
    ordering = ['orden']

class SeguimientoFaseInline(admin.TabularInline):
    model = SeguimientoFase
    extra = 0
    fields = ['fase', 'completado', 'fecha_inicio', 'fecha_conclusion']
    readonly_fields = ['fase']

@admin.register(RediseñoCurricular)
class RediseñoCurricularAdmin(admin.ModelAdmin):
    list_display = ['carrera', 'año', 'estado', 'progreso_porcentaje', 'actualizado_el']
    list_filter = ['estado', 'año', 'carrera__sede']
    search_fields = ['carrera__nombre']
    inlines = [SeguimientoFaseInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
        
        # Crear automáticamente los seguimientos para todas las fases
        if not change:
            fases = Fase.objects.all()
            for fase in fases:
                SeguimientoFase.objects.get_or_create(
                    rediseño=obj,
                    fase=fase
                )

@admin.register(SeguimientoFase)
class SeguimientoFaseAdmin(admin.ModelAdmin):
    list_display = ['rediseño', 'fase', 'completado', 'fecha_inicio', 'fecha_conclusion']
    list_filter = ['completado', 'fase', 'rediseño__carrera__sede']
    search_fields = ['rediseño__carrera__nombre']

@admin.register(ArchivoComisionAcademica)
class ArchivoComisionAcademicaAdmin(admin.ModelAdmin):
    list_display = ['nombre_original', 'seguimiento', 'tamaño_legible', 'subido_por', 'subido_el']
    list_filter = ['subido_el']
    search_fields = ['nombre_original', 'seguimiento__rediseño__carrera__nombre']
    readonly_fields = ['tamaño', 'tipo_mime', 'subido_por', 'subido_el']