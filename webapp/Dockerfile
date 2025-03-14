FROM python:3-slim

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cria o diretório da aplicação
WORKDIR /app

# Copia todo o conteúdo do diretório atual (que já é o diretório webagenda) para /app
COPY . /app
COPY webagenda /app/webagenda

RUN pip install --upgrade pip

# Instala as dependências
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/staticfiles

# Cria o entrypoint.sh diretamente no Dockerfile
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'python manage.py migrate' >> /app/entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput' >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Cria o super usuário
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'python manage.py migrate' >> /app/entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput' >> /app/entrypoint.sh && \
    echo 'DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=admin123 python manage.py createsuperuser --noinput || true' >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh


# Adiciona o diretório raiz ao PYTHONPATH
ENV PYTHONPATH="/app"

# Define o usuário não root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Usa o novo entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Executa o projeto no Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]