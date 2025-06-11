from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ui.urls')),  # Route for the main UI
    path('auth/', include('authentication.urls')),
    # path('dashboard/', include('ui.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),  
    path('api/', include('api.urls')),
]
=======
from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static

assets_dir = Path(settings.BASE_DIR) / "ui" / "static" / "sneat" / "assets"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ui.urls")),
    path("accounts/", include("authentication.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static("/assets/", document_root=assets_dir)
>>>>>>> 7576c1d35bb7910344a6ac3a18c4a6d539cb55fd
