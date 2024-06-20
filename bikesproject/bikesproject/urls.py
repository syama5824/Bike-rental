from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from bikes.views import UserFormView,home
from rest_framework.authtoken import views

urlpatterns = [
    path('',home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('bikes.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('bikes/', include('bikes.urls')),
    # path('contact/', UserFormView.as_view(), name='contact-form'),
    # path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
