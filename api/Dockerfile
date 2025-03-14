FROM python:3-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crie o diretório da aplicação
WORKDIR /app

# Copie todo o conteúdo do diretório atual (que já é o diretório api) para /app
COPY . /app

RUN pip install --upgrade pip

# Instale as dependências
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/staticfiles

# Crie o entrypoint.sh diretamente no Dockerfile
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

# Adicione o diretório raiz ao PYTHONPATH
ENV PYTHONPATH="/app"

# Define o usuário não root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Use o novo entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Execute o projeto no Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]