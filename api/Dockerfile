FROM python:3-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crie o diretório da aplicação
WORKDIR /app

# Copie o conteúdo do diretório api para dentro de /app/api
COPY . /app

RUN pip install --upgrade pip

# Instale as dependências
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

RUN python /app/manage.py collectstatic --noinput

# Adicione o diretório raiz ao PYTHONPATH
ENV PYTHONPATH="/app"

# Define o usuário não root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Execute o projeto no guinicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]