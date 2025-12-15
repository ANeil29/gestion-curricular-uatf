from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Sede(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Facultad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    GRADO_CHOICES = [
        ('licenciatura', 'Licenciatura'),
        ('tecnico_superior', 'Técnico Superior'),
        ('tecnico_medio', 'Técnico Medio'),
    ]
    
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carreras')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='carreras')
    nombre = models.CharField(max_length=200)
    grado_academico = models.CharField(max_length=20, choices=GRADO_CHOICES, default='licenciatura')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ['sede', 'facultad', 'nombre']
        unique_together = ['facultad', 'sede', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.sede.nombre}"

class Fase(models.Model):
    numero = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Fase"
        verbose_name_plural = "Fases"
        ordering = ['orden', 'numero']
    
    def __str__(self):
        return f"{self.numero}. {self.nombre} ({self.codigo})"

class RediseñoCurricular(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='rediseños')
    año = models.IntegerField(default=2025)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_conclusion = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('en_proceso', 'En Proceso'),
            ('completado', 'Completado'),
            ('suspendido', 'Suspendido'),
        ],
        default='en_proceso'
    )
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rediseños_creados')
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Rediseño Curricular"
        verbose_name_plural = "Rediseños Curriculares"
        ordering = ['-año', 'carrera']
        unique_together = ['carrera', 'año']
    
    def __str__(self):
        return f"Rediseño {self.año} - {self.carrera}"
    
    def progreso_porcentaje(self):
        total_fases = 10
        fases_completadas = self.seguimientos.filter(completado=True).count()
        return int((fases_completadas / total_fases) * 100)

class SeguimientoFase(models.Model):
    rediseño = models.ForeignKey(RediseñoCurricular, on_delete=models.CASCADE, related_name='seguimientos')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_conclusion = models.DateField(null=True, blank=True)
    medio_verificacion = models.TextField(blank=True, help_text="Descripción del medio de verificación")
    observaciones = models.TextField(blank=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seguimientos_actualizados')
    actualizado_el = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Seguimiento de Fase"
        verbose_name_plural = "Seguimientos de Fases"
        ordering = ['rediseño', 'fase__orden']
        unique_together = ['rediseño', 'fase']
    
    def __str__(self):
        return f"{self.rediseño} - {self.fase.nombre}"

class ArchivoComisionAcademica(models.Model):
    seguimiento = models.ForeignKey(
        SeguimientoFase, 
        on_delete=models.CASCADE, 
        related_name='archivos',
        limit_choices_to={'fase__codigo': 'CA'}
    )
    archivo = models.FileField(upload_to='comision_academica/%Y/%m/')
    nombre_original = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=500, blank=True)
    tamaño = models.IntegerField(help_text="Tamaño en bytes")
    tipo_mime = models.CharField(max_length=100)
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subido_el = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Archivo Comisión Académica"
        verbose_name_plural = "Archivos Comisión Académica"
        ordering = ['-subido_el']
    
    def __str__(self):
        return f"{self.nombre_original} - {self.seguimiento.rediseño.carrera}"
    
    def tamaño_legible(self):
        """Retorna el tamaño del archivo en formato legible"""
        tamaño = self.tamaño
        for unidad in ['bytes', 'KB', 'MB', 'GB']:
            if tamaño < 1024.0:
                return f"{tamaño:.1f} {unidad}"
            tamaño /= 1024.0
        return f"{tamaño:.1f} TB"