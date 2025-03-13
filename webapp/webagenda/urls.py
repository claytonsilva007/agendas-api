from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_agendas, name="listar_agendas"),
    path("criar/", views.criar_agenda, name="criar_agenda"),
    path("editar/<int:id>/", views.editar_agenda, name="editar_agenda"),
    path("deletar/<int:id>/", views.deletar_agenda, name="deletar_agenda"),
]
