FROM python:3.12-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app /app

# Устанавливаем виртуальное окружение и зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем сервер FastAPI с использованием uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
