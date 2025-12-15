from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),  # Redirige / a login
    path('curricular/', include('curricular.urls', namespace='curricular')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalizar admin
admin.site.site_header = "Sistema de Gestión Curricular UATF"
admin.site.site_title = "Gestión Curricular"
admin.site.index_title = "Panel de Administración"