from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # URLs existentes
    path("", views.listar_agendas, name="listar_agendas"),
    path("criar/", views.gerenciar_agenda, name="gerenciar_agenda"),
    path("gerenciar_agenda/<int:id>/", views.gerenciar_agenda, name="gerenciar_agenda"),
    path("deletar/<int:id>/", views.deletar_agenda, name="deletar_agenda"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # URLs de redefinição de senha
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
