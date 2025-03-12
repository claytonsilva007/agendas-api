FROM python:3-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crie o diretório da aplicação
WORKDIR /app

# Copie o conteúdo do diretório api para dentro de /app
COPY . /app

RUN pip install --upgrade pip

# Instale as dependências
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Adicione o entrypoint script
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Adicione o diretório raiz ao PYTHONPATH
ENV PYTHONPATH="/app"

# Define o usuário não root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Defina o entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Execute o projeto no Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
