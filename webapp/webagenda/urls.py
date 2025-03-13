from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_agendas, name="listar_agendas"),
    path("criar/", views.gerenciar_agenda, name="gerenciar_agenda"),
    path("gerenciar_agenda/<int:id>/", views.gerenciar_agenda, name="gerenciar_agenda"),
    path("deletar/<int:id>/", views.deletar_agenda, name="deletar_agenda"),
]
