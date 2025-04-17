# Python 3.12 bazaviy imidj
FROM python:3.12-slim

# Ishchi papka
WORKDIR /app

# requirements.txt faylini nusxalab, kutubxonalarni o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Butun loyiha fayllarini konteynerga ko‘chiramiz
COPY . .

# Django runserver va Telegram botni bir vaqtda ishga tushiramiz
CMD ["sh", "-c", "python manage.py bot"]
