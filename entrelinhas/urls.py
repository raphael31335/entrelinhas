from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),          # home, register
    path('livros/', include('livros.urls')), # app livros
    path('', include('django.contrib.auth.urls')),  # login/logout (names: login, logout, password_* )
]
