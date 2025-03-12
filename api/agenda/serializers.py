from rest_framework import serializers
from .models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda  # Correção: use "=" ao invés de ":"
        fields = '__all__'
