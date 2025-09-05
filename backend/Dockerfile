FROM python:3.9

WORKDIR /app

COPY requirements.txt .

# Устанавливаем зависимости для Pillow и другие необходимые пакеты
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Делаем startup скрипт исполняемым
RUN chmod +x startup.sh

CMD ["./startup.sh"] 