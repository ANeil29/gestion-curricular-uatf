from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('coordinador', 'Coordinador de Carrera'),
        ('gestor', 'Gestor Curricular'),
        ('revisor', 'Revisor'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='revisor')
    telefono = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    facultad = models.ForeignKey(
        'curricular.Facultad', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
    
    def puede_editar(self):
        return self.rol in ['admin', 'coordinador', 'gestor']