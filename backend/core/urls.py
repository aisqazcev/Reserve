from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('reserve/', include('reserve.urls', namespace="reserve")),
    
    path('api-auth/', include('rest_framework.urls')),

    # path("token/", TokenObtainPairView.as_view(), name="obtain_token"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),

    path('', include('reserve.urls', namespace="api")),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)