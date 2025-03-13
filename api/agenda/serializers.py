from rest_framework import serializers
from .models import Agenda
from datetime import datetime, timedelta

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

    def validate_dataInicio(self, value):
        return self._round_time(value)

    def validate_dataFim(self, value):
        return self._round_time(value)

    def validate(self, data):
        data_inicio = data.get('dataInicio')
        data_fim = data.get('dataFim')

        # Garante que data_fim seja pelo menos 15 minutos após data_inicio
        if data_fim <= data_inicio:
            data_fim = data_inicio + timedelta(minutes=15)
            data['dataFim'] = data_fim

        return data

    def _round_time(self, dt):
        minute = dt.minute
        if minute % 15 != 0:
            if minute < 8:
                dt = dt.replace(minute=0, second=0, microsecond=0)
            elif minute < 23:
                dt = dt.replace(minute=15, second=0, microsecond=0)
            elif minute < 38:
                dt = dt.replace(minute=30, second=0, microsecond=0)
            else:
                dt = dt.replace(minute=45, second=0, microsecond=0)
        return dt
