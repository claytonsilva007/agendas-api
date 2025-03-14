from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from agenda import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Para obter o access_token e refresh_token
    TokenRefreshView      # Para renovar o access_token
)


urlpatterns = [
    path('agenda/', views.AgendaList.as_view()),
    path('agenda/<int:pk>/', views.AgendaDetail.as_view()),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)