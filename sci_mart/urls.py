from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import api_root_view

schema_view = get_schema_view(
   openapi.Info(
      title="SciMart E-Commarce API",
      default_version='v1',
      description="API Documentation for SciMart E-commarce Project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@scimart.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root_view),
    path('api/v1/', include('api.urls'), name='api-root'),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
