# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем необходимые системные зависимости (если требуется, например, для psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .


