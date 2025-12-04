# Imagem base
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências de sistema necessárias (opcional, mas comum)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências primeiro (para aproveitar cache)
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expondo porta do Flask
EXPOSE 5000

# Variáveis opcionais — podem ser sobrescritas no docker-compose
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Comando padrão para rodar o Flask
CMD ["python", "app.py"]
