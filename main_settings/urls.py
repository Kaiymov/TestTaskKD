from django.contrib import admin
from django.urls import path, re_path, include

from djoser.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account_register/', UserViewSet.as_view({'post': 'create'}), name="register"),
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken')),
    path('', include('account_api.urls')),
]
