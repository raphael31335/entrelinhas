from django.contrib import admin
from django.urls import path, include

# Importações necessárias para arquivos estáticos no modo DEBUG
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),           # URLs da parte principal do site
    path('livros/', include('livros.urls')),  # URLs do app livros
]

# Somente adiciona os arquivos estáticos se estiver no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
