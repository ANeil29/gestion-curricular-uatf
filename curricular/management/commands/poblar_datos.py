from django.core.management.base import BaseCommand
from curricular.models import Sede, Facultad, Carrera, Fase, RediseñoCurricular, SeguimientoFase

class Command(BaseCommand):
    help = 'Poblar la base de datos con información inicial de la UATF'

    def handle(self, *args, **kwargs):
        self.stdout.write('Poblando base de datos...')
        
        # Crear Sedes
        self.crear_sedes()
        
        # Crear Facultades
        self.crear_facultades()
        
        # Crear Fases del Rediseño Curricular
        self.crear_fases()
        
        # Crear Carreras
        self.crear_carreras_potosi()
        self.crear_carreras_sedes_regionales()
        
        self.stdout.write(self.style.SUCCESS('✅ Base de datos poblada exitosamente!'))
    
    def crear_sedes(self):
        sedes = [
            'Potosí',
            'Tupiza',
            'Villazón',
            'Uyuni',
            'Uncía',
            'Llica',
            'San Cristóbal',
            'Río Grande'
        ]
        
        for nombre in sedes:
            sede, created = Sede.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(f'✅ Sede creada: {nombre}')
    
    def crear_facultades(self):
        facultades = [
            'Facultad de Artes',
            'Facultad de Ciencias Agrícolas y Pecuarias',
            'Facultad de Ciencias Económicas, Financieras y Administrativas',
            'Facultad de Ciencias Puras',
            'Facultad de Ciencias Sociales y Humanísticas',
            'Facultad de Derecho',
            'Facultad de Ingeniería',
            'Facultad de Ingeniería Geológica',
            'Facultad de Ingeniería Minera',
            'Facultad de Ingeniería Tecnológica',
            'Facultad de Ciencias de la Salud',
            'Facultad de Medicina',
            'Vicerrectorado'
        ]
        
        for nombre in facultades:
            facultad, created = Facultad.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(f'✅ Facultad creada: {nombre}')
    
    def crear_fases(self):
        fases_data = [
            (1, 'Organización en Comisión de Rediseño Curricular', 'RC', 1),
            (2, 'Recolección de Documentos y Proyecto Curricular', 'PC', 2),
            (3, 'Diagnóstico Inicial de la Carrera', 'DI', 3),
            (4, 'Estudio de Contexto', 'EC', 4),
            (5, 'Mesa Multisectorial', 'MM', 5),
            (6, 'Elaboración de la Propuesta Macro Curricular', 'MC', 6),
            (7, 'Reunión Académica de Carrera', 'RAC', 7),
            (8, 'Validación Técnica', 'VT', 8),
            (9, 'Validación Normativa', 'VN', 9),
            (10, 'Comisión Académica', 'CA', 10),
            (11, 'Honorable Consejo Universitario', 'HCU', 11),
            (12, 'Reunión Académica Nacional', 'RAN', 12),
        ]
        
        for numero, nombre, codigo, orden in fases_data:
            fase, created = Fase.objects.get_or_create(
                numero=numero,
                defaults={
                    'nombre': nombre,
                    'codigo': codigo,
                    'orden': orden
                }
            )
            if created:
                self.stdout.write(f'✅ Fase creada: {nombre}')
    
    def crear_carreras_potosi(self):
        potosi = Sede.objects.get(nombre='Potosí')
        
        carreras_potosi = [
            # Facultad de Artes
            ('Facultad de Artes', 'Artes Musicales', 'licenciatura'),
            ('Facultad de Artes', 'Artes Plásticas', 'licenciatura'),
            ('Facultad de Artes', 'Arquitectura', 'licenciatura'),
            
            # Facultad de Ciencias Agrícolas y Pecuarias
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agronómica', 'licenciatura'),
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agroindustrial', 'licenciatura'),
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería en Desarrollo Rural', 'licenciatura'),
            
            # Facultad de Ciencias Económicas, Financieras y Administrativas
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Auditoría - Contaduría Pública', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Contabilidad y Finanzas', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Administración de Empresas', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Ingeniería Comercial', 'licenciatura'),
            
            # Facultad de Ciencias Puras
            ('Facultad de Ciencias Puras', 'Química', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Estadística', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Física', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Matemática', 'licenciatura'),
            ('Facultad de Ciencias Puras', 'Ingeniería Informática', 'licenciatura'),
            
            # Facultad de Ciencias Sociales y Humanísticas
            ('Facultad de Ciencias Sociales y Humanísticas', 'Turismo', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Trabajo Social', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Programa de Ciencias de la Comunicación', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Programa de Pedagogía Intercultural', 'licenciatura'),
            
            # Facultad de Derecho
            ('Facultad de Derecho', 'Derecho', 'licenciatura'),
            
            # Facultad de Ingeniería
            ('Facultad de Ingeniería', 'Ingeniería Civil', 'licenciatura'),
            ('Facultad de Ingeniería', 'Construcciones Civiles', 'tecnico_superior'),
            ('Facultad de Ingeniería', 'Ingeniería en Geodesia y Topografía', 'licenciatura'),
            
            # Facultad de Ingeniería Geológica
            ('Facultad de Ingeniería Geológica', 'Ingeniería Geológica', 'licenciatura'),
            ('Facultad de Ingeniería Geológica', 'Ingeniería del Medio Ambiente', 'licenciatura'),
            
            # Facultad de Ingeniería Minera
            ('Facultad de Ingeniería Minera', 'Ingeniería Minera', 'licenciatura'),
            ('Facultad de Ingeniería Minera', 'Ingeniería de Procesos de Materias Primas Minerales', 'licenciatura'),
            
            # Facultad de Ingeniería Tecnológica
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Eléctrica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Electrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecánica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecatrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Mecánica Automotriz', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Electricidad', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Electrónica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecánica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecatrónica', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Técnico Univ. Medio en Mecánica Automotriz', 'tecnico_medio'),
            
            # Facultad de Ciencias de la Salud
            ('Facultad de Ciencias de la Salud', 'Enfermería', 'licenciatura'),
            ('Facultad de Ciencias de la Salud', 'Técnico Univ. Medio Auxiliar de Enfermería', 'tecnico_medio'),
            
            # Facultad de Medicina
            ('Facultad de Medicina', 'Medicina', 'licenciatura'),
            
            # Vicerrectorado
            ('Vicerrectorado', 'Programa Enfermeria', 'licenciatura'),
            ('Vicerrectorado', 'Programa Derecho', 'licenciatura'),
            ('Vicerrectorado', 'Programa Ciencias de la Comunicación', 'licenciatura'),
            ('Vicerrectorado', 'Odontologia', 'licenciatura'),
            ('Vicerrectorado', 'Ingeniería de Sistemas', 'licenciatura'),
            ('Vicerrectorado', 'Programa Diseño y Programacion Digital', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_potosi:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            carrera, created = Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=potosi,
                defaults={'grado_academico': grado}
            )
            if created:
                self.stdout.write(f"✅ Creada: {carrera_nombre} - {facultad_nombre} - Potosí")
    
    def crear_carreras_sedes_regionales(self):
        # Tupiza
        tupiza = Sede.objects.get(nombre='Tupiza')
        carreras_tupiza = [
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Medicina Veterinaria y Zootecnia', 'licenciatura'),
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Contaduría Pública', 'licenciatura'),
            ('Vicerrectorado', 'Programa Derecho', 'licenciatura'),
            ('Vicerrectorado', 'Ingeniería de Sistemas', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Escuela de Idiomas', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_tupiza:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=tupiza,
                defaults={'grado_academico': grado}
            )
        
        # Villazón
        villazon = Sede.objects.get(nombre='Villazón')
        carreras_villazon = [
            ('Facultad de Ciencias Agrícolas y Pecuarias', 'Ingeniería Agropecuaria', 'licenciatura'),
            ('Facultad de Ciencias de la Salud', 'Enfermería', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_villazon:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=villazon,
                defaults={'grado_academico': grado}
            )
        
        # Uyuni
        uyuni = Sede.objects.get(nombre='Uyuni')
        carreras_uyuni = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Turismo', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_uyuni:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=uyuni,
                defaults={'grado_academico': grado}
            )
        
        # Uncía
        uncia = Sede.objects.get(nombre='Uncía')
        carreras_uncia = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Economía', 'licenciatura'),
            ('Facultad de Derecho', 'Derecho', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Trabajo Social', 'licenciatura'),
            ('Facultad de Ciencias Sociales y Humanísticas', 'Lingüística e Idiomas', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_uncia:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=uncia,
                defaults={'grado_academico': grado}
            )
        
        # Llica
        llica = Sede.objects.get(nombre='Llica')
        carreras_llica = [
            ('Vicerrectorado', 'Programa Enfermeria', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_llica:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=llica,
                defaults={'grado_academico': grado}
            )
        
        # San Cristóbal
        san_cristobal = Sede.objects.get(nombre='San Cristóbal')
        carreras_san_cristobal = [
            ('Facultad de Ciencias de la Salud', 'Técnico Univ. Medio Auxiliar de Enfermería', 'tecnico_medio'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Eléctrica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecánica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Mecatrónica', 'licenciatura'),
            ('Facultad de Ingeniería Tecnológica', 'Ingeniería Automotriz', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_san_cristobal:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=san_cristobal,
                defaults={'grado_academico': grado}
            )
        
        # Río Grande
        rio_grande = Sede.objects.get(nombre='Río Grande')
        carreras_rio_grande = [
            ('Facultad de Ciencias Económicas, Financieras y Administrativas', 'Administración de Empresas', 'licenciatura'),
        ]
        
        for facultad_nombre, carrera_nombre, grado in carreras_rio_grande:
            facultad = Facultad.objects.get(nombre=facultad_nombre)
            Carrera.objects.get_or_create(
                facultad=facultad,
                nombre=carrera_nombre,
                sede=rio_grande,
                defaults={'grado_academico': grado}
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Todas las carreras han sido creadas!'))