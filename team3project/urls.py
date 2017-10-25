from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from sports.views import login_view, logout_view, register_view


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
     url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^', include('sports.urls', namespace='sports')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)