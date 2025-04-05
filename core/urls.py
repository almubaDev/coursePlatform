from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('users/', include('users.urls', namespace='users')),
    # path('courses/', include('courses.urls', namespace='courses')),
    # path('tools/', include('tools.urls', namespace='tools')),
    # path('subscription/', include('subscription.urls', namespace='subscription')),
]

# Configuración para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)