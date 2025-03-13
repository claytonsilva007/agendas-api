from django.db import models


class EstadoAgenda(models.TextChoices):
    RECEBIDO = "RECEBIDO", "Recebido"
    CONFIRMADO = "CONFIRMADO", "Confirmado"
    ATENDIDO = "ATENDIDO", "Atendido"
    CANCELADO = "CANCELADO", "Cancelado"
    

class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    dataInicio = models.DateTimeField()
    dataFim = models.DateTimeField()
    local = models.CharField(max_length=100)
    
    estado_atual = models.CharField(
        max_length=10,
        choices=EstadoAgenda.choices,
        default=EstadoAgenda.RECEBIDO
    )
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['dataInicio']
        
        
