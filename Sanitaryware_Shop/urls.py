
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path
from django.urls.conf import include
from django.conf import settings

admin.site.unregister(Group)

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('securelogin/', admin.site.urls),
    # path('baton/', include('baton.urls')),

    path('login/admin/', admin.site.urls,name='admin'),
    path('',include('accounts.urls')),
    path('',include('shop_app.urls')),
    path('', include('User_Dashboard.urls')),
    path('', include('orders.urls')),
    path('', include('variations.urls')),


    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
