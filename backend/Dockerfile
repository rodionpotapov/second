# # Указываем базовый образ
# FROM python:3.10-slim-bullseye

# # Устанавливаем переменные окружения
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Создаем рабочую директорию
# WORKDIR /app

# # Копируем файлы requirements.txt и устанавливаем зависимости
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Копируем остальные файлы приложения
# COPY . /app/

# # Открываем порт, если это необходимо для вашего приложения (например, для Django)
# EXPOSE 8000

# # Команда для запуска вашего приложения (замените на вашу команду запуска)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]





FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev
RUN apt-get install -y gobject-introspection
RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .