from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('webagenda/admin/', admin.site.urls),
    path("webagenda/", include("webagenda.urls")),
]

