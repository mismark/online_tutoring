from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.accounts import views


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", views.home, name="home"),

    path("dashboard/", include("apps.dashboard.urls")),
    path("accounts/", include("apps.accounts.urls")),
    # Courses
    path("courses/", include("apps.courses.urls")),
    path(
    "certificates/",
    include("apps.certificates.urls"),
),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
    