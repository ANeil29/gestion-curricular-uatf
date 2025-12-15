from django import forms
from .models import SeguimientoFase, ArchivoComisionAcademica

class SeguimientoFaseForm(forms.ModelForm):
    class Meta:
        model = SeguimientoFase
        fields = [
            'completado', 
            'fecha_inicio', 
            'fecha_conclusion', 
            'medio_verificacion', 
            'observaciones'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_conclusion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medio_verificacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'completado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'completado': 'Fase Completada',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_conclusion': 'Fecha de Conclusión',
            'medio_verificacion': 'Medio de Verificación',
            'observaciones': 'Observaciones',
        }

class ArchivoComisionAcademicaForm(forms.ModelForm):
    class Meta:
        model = ArchivoComisionAcademica
        fields = ['archivo', 'descripcion']
        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del archivo (opcional)'}),
        }
        labels = {
            'archivo': 'Seleccionar Archivo',
            'descripcion': 'Descripción',
        }
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño máximo (50MB)
            if archivo.size > 50 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 50MB')
            
            # Validar extensiones permitidas
            extensiones_permitidas = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                '.ppt', '.pptx', '.txt', '.zip', '.rar'
            ]
            nombre = archivo.name.lower()
            if not any(nombre.endswith(ext) for ext in extensiones_permitidas):
                raise forms.ValidationError(
                    'Formato de archivo no permitido. Formatos aceptados: PDF, Word, Excel, PowerPoint, TXT, ZIP, RAR'
                )
        return archivo