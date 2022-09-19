
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home_app.urls')),
    path('fyh/',include('shop.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
