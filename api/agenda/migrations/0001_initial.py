# Generated by Django 5.1.7 on 2025-03-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('dataInicio', models.DateTimeField()),
                ('dataFim', models.DateTimeField()),
                ('local', models.CharField(max_length=100)),
                ('estado_atual', models.CharField(choices=[('RECEBIDO', 'Recebido'), ('CONFIRMADO', 'Confirmado'), ('ATENDIDO', 'Atendido'), ('CANCELADO', 'Cancelado')], default='RECEBIDO', max_length=10)),
            ],
            options={
                'ordering': ['dataInicio'],
            },
        ),
    ]
