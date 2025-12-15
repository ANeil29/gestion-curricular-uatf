from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import mimetypes

from .models import (
    RediseñoCurricular, SeguimientoFase, Carrera, Fase, 
    ArchivoComisionAcademica, Sede, Facultad
)
from .forms import SeguimientoFaseForm, ArchivoComisionAcademicaForm

@login_required
def dashboard(request):
    """Dashboard principal con estadísticas"""
    total_carreras = Carrera.objects.filter(activo=True).count()
    total_rediseños = RediseñoCurricular.objects.filter(estado='en_proceso').count()
    
    # Rediseños por sede
    rediseños_por_sede = RediseñoCurricular.objects.filter(
        estado='en_proceso'
    ).values('carrera__sede__nombre').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Últimos rediseños actualizados
    ultimos_rediseños = RediseñoCurricular.objects.select_related(
        'carrera', 'carrera__sede', 'carrera__facultad'
    ).order_by('-actualizado_el')[:10]
    
    context = {
        'total_carreras': total_carreras,
        'total_rediseños': total_rediseños,
        'rediseños_por_sede': rediseños_por_sede,
        'ultimos_rediseños': ultimos_rediseños,
    }
    return render(request, 'curricular/dashboard.html', context)

@login_required
def lista_carreras(request):
    """Lista de todas las carreras con filtros"""
    carreras = Carrera.objects.select_related('facultad', 'sede').filter(activo=True)
    
    # Filtros
    sede_id = request.GET.get('sede')
    facultad_id = request.GET.get('facultad')
    buscar = request.GET.get('buscar')
    
    if sede_id:
        carreras = carreras.filter(sede_id=sede_id)
    if facultad_id:
        carreras = carreras.filter(facultad_id=facultad_id)
    if buscar:
        carreras = carreras.filter(
            Q(nombre__icontains=buscar) |
            Q(facultad__nombre__icontains=buscar)
        )
    
    # Paginación
    paginator = Paginator(carreras, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'sedes': Sede.objects.all(),
        'facultades': Facultad.objects.all(),
    }
    return render(request, 'curricular/lista_carreras.html', context)

@login_required
def detalle_rediseño(request, rediseño_id):
    """Detalle del rediseño curricular con sus fases"""
    rediseño = get_object_or_404(
        RediseñoCurricular.objects.select_related(
            'carrera', 'carrera__sede', 'carrera__facultad'
        ),
        id=rediseño_id
    )
    
    seguimientos = rediseño.seguimientos.select_related('fase').order_by('fase__orden')
    
    context = {
        'rediseño': rediseño,
        'seguimientos': seguimientos,
    }
    return render(request, 'curricular/detalle_rediseño.html', context)

@login_required
def actualizar_fase(request, seguimiento_id):
    """Actualizar el estado de una fase"""
    seguimiento = get_object_or_404(SeguimientoFase, id=seguimiento_id)
    
    if not request.user.puede_editar():
        messages.error(request, 'No tienes permisos para editar esta fase.')
        return redirect('curricular:detalle_rediseño', rediseño_id=seguimiento.rediseño.id)
    
    if request.method == 'POST':
        form = SeguimientoFaseForm(request.POST, instance=seguimiento)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.actualizado_por = request.user
            seguimiento.save()
            messages.success(request, 'Fase actualizada correctamente.')
            return redirect('curricular:detalle_rediseño', rediseño_id=seguimiento.rediseño.id)
    else:
        form = SeguimientoFaseForm(instance=seguimiento)
    
    context = {
        'form': form,
        'seguimiento': seguimiento,
    }
    return render(request, 'curricular/actualizar_fase.html', context)

@login_required
def subir_archivo_ca(request, seguimiento_id):
    """Subir archivo para la fase Comisión Académica"""
    seguimiento = get_object_or_404(SeguimientoFase, id=seguimiento_id, fase__codigo='CA')
    
    if not request.user.puede_editar():
        messages.error(request, 'No tienes permisos para subir archivos.')
        return redirect('curricular:detalle_rediseño', rediseño_id=seguimiento.rediseño.id)
    
    if request.method == 'POST':
        form = ArchivoComisionAcademicaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.seguimiento = seguimiento
            archivo.subido_por = request.user
            
            # Obtener información del archivo
            archivo_obj = request.FILES['archivo']
            archivo.nombre_original = archivo_obj.name
            archivo.tamaño = archivo_obj.size
            archivo.tipo_mime = archivo_obj.content_type or 'application/octet-stream'
            
            archivo.save()
            messages.success(request, 'Archivo subido correctamente.')
            return redirect('curricular:detalle_rediseño', rediseño_id=seguimiento.rediseño.id)
    else:
        form = ArchivoComisionAcademicaForm()
    
    context = {
        'form': form,
        'seguimiento': seguimiento,
        'archivos_existentes': seguimiento.archivos.all(),
    }
    return render(request, 'curricular/subir_archivo_ca.html', context)

@login_required
def descargar_archivo_ca(request, archivo_id):
    """Descargar archivo de Comisión Académica"""
    archivo = get_object_or_404(ArchivoComisionAcademica, id=archivo_id)
    
    # Servir el archivo
    response = FileResponse(archivo.archivo.open('rb'))
    response['Content-Type'] = archivo.tipo_mime
    response['Content-Disposition'] = f'attachment; filename="{archivo.nombre_original}"'
    
    return response

@login_required
def eliminar_archivo_ca(request, archivo_id):
    """Eliminar archivo de Comisión Académica"""
    archivo = get_object_or_404(ArchivoComisionAcademica, id=archivo_id)
    
    if not request.user.puede_editar():
        messages.error(request, 'No tienes permisos para eliminar archivos.')
        return redirect('curricular:detalle_rediseño', rediseño_id=archivo.seguimiento.rediseño.id)
    
    if request.method == 'POST':
        rediseño_id = archivo.seguimiento.rediseño.id
        archivo.archivo.delete()
        archivo.delete()
        messages.success(request, 'Archivo eliminado correctamente.')
        return redirect('curricular:detalle_rediseño', rediseño_id=rediseño_id)
    
    context = {'archivo': archivo}
    return render(request, 'curricular/confirmar_eliminar_archivo.html', context)

@login_required
def generar_reporte_pdf(request):
    """Generar reporte PDF del estado de todos los rediseños"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_rediseño_curricular.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Título
    title = Paragraph("REPORTE DE REDISEÑO CURRICULAR 2025<br/>UATF - POTOSÍ", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Estadísticas generales
    total_carreras = Carrera.objects.filter(activo=True).count()
    total_rediseños = RediseñoCurricular.objects.filter(estado='en_proceso').count()
    
    stats_data = [
        ['Total de Carreras:', str(total_carreras)],
        ['Rediseños en Proceso:', str(total_rediseños)],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de rediseños por sede
    rediseños = RediseñoCurricular.objects.select_related(
        'carrera__sede', 'carrera__facultad'
    ).filter(estado='en_proceso').order_by('carrera__sede__nombre', 'carrera__nombre')
    
    for sede in Sede.objects.all():
        rediseños_sede = rediseños.filter(carrera__sede=sede)
        if not rediseños_sede.exists():
            continue
        
        elements.append(Paragraph(f"<b>SEDE: {sede.nombre.upper()}</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        data = [['#', 'Carrera', 'Facultad', 'Progreso']]
        
        for idx, rediseño in enumerate(rediseños_sede, 1):
            data.append([
                str(idx),
                rediseño.carrera.nombre,
                rediseño.carrera.facultad.nombre[:30] + '...' if len(rediseño.carrera.facultad.nombre) > 30 else rediseño.carrera.facultad.nombre,
                f"{rediseño.progreso_porcentaje()}%"
            ])
        
        table = Table(data, colWidths=[0.5*inch, 2.5*inch, 2.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response