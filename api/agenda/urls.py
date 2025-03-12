from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from agenda import views

urlpatterns = [
    path('agenda/', views.AgendaList.as_view()),
    path('agenda/<int:pk>/', views.AgendaDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)