🎓 Sistema de Gestión Curricular UATF
Sistema web para el seguimiento y gestión del rediseño curricular de la Universidad Autónoma Tomás Frías de Potosí, Bolivia.
📋 Características

✅ Gestión de 70 carreras en 8 sedes diferentes
✅ Seguimiento de 12 fases del proceso de rediseño curricular
✅ Sistema de autenticación con roles y permisos
✅ Carga y descarga de archivos para la fase de Comisión Académica
✅ Generación de reportes PDF con el estado de todos los rediseños
✅ Dashboard con estadísticas en tiempo real
✅ Filtros y búsqueda avanzada de carreras
✅ Interfaz responsive y moderna

🛠️ Tecnologías Utilizadas

Backend: Django 4.2+
Base de Datos: SQLite (desarrollo) / PostgreSQL (producción)
Frontend: Bootstrap 5, Font Awesome
Reportes: ReportLab (PDF)
Archivos: Pillow, Python-Decouple

📦 Instalación Local
Requisitos Previos

Python 3.10 o superior
pip (gestor de paquetes de Python)
Git

Pasos de Instalación

Clonar el repositorio

bashgit clone https://github.com/tu-usuario/gestion-curricular-uatf.git
cd gestion-curricular-uatf

Crear y activar entorno virtual

bashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

Instalar dependencias

bashpip install -r requirements.txt

Configurar variables de entorno
Crea un archivo .env en la raíz:

SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

Aplicar migraciones

bashpython manage.py makemigrations
python manage.py migrate

Poblar base de datos

bashpython manage.py poblar_datos

Crear superusuario

bashpython manage.py createsuperuser

Recolectar archivos estáticos

bashpython manage.py collectstatic --noinput

Ejecutar servidor de desarrollo

bashpython manage.py runserver
Accede a: http://127.0.0.1:8000
📂 Estructura del Proyecto
gestion-curricular-uatf/
├── config/              # Configuración principal
├── accounts/            # App de autenticación
├── curricular/          # App principal de gestión
├── templates/           # Templates HTML
├── static/              # Archivos estáticos
├── media/               # Archivos subidos
├── requirements.txt     # Dependencias
└── manage.py           # Script de gestión
👥 Roles de Usuario

Administrador: Acceso completo al sistema
Coordinador: Gestión de carreras y fases
Gestor Curricular: Edición de seguimientos
Revisor: Solo lectura

📊 Fases del Rediseño Curricular

Organización en Comisión de Rediseño Curricular (RC)
Recolección de Documentos y Proyecto Curricular (PC)
Diagnóstico Inicial de la Carrera (DI)
Estudio de Contexto (EC)
Mesa Multisectorial (MM)
Elaboración de la Propuesta Macro Curricular (MC)
Reunión Académica de Carrera (RAC)
Validación Técnica (VT)
Validación Normativa (VN)
Comisión Académica (CA) - Con gestión de archivos
Honorable Consejo Universitario (HCU)
Reunión Académica Nacional (RAN)

🚀 Deployment en Producción
Opción 1: PythonAnywhere (Gratis)
Ver guía completa en GUÍA_PRODUCCIÓN.md
Opción 2: Render.com

Conecta tu repositorio de GitHub
Render detectará automáticamente render.yaml
Click en "Deploy"

Opción 3: Railway.app

Importa tu repositorio
Railway configurará automáticamente
Agrega variables de entorno

🔐 Seguridad

Variables de entorno para información sensible
CSRF protection habilitado
Autenticación requerida para todas las vistas
Permisos basados en roles
Validación de archivos subidos

📝 Comandos Útiles
bash# Crear superusuario
python manage.py createsuperuser

# Poblar base de datos
python manage.py poblar_datos

# Hacer backup
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Limpiar archivos estáticos
python manage.py collectstatic --clear

# Crear migraciones
python manage.py makemigrations

# Ver SQL de migraciones
python manage.py sqlmigrate curricular 0001
🐛 Solución de Problemas
Error: No module named 'curricular'
bashpython manage.py makemigrations curricular
python manage.py migrate
Error: Static files not found
bashpython manage.py collectstatic --noinput
Error al subir archivos
Verifica permisos de la carpeta media:
bashchmod 755 media/
📄 Licencia
Este proyecto es de uso interno de la Universidad Autónoma Tomás Frías.
👨‍💻 Autor
Desarrollado para el Departamento de Gestión Curricular - UATF
📞 Contacto
Para soporte técnico, contactar al Departamento de Gestión Curricular.

Universidad Autónoma Tomás Frías - Potosí, Bolivia
