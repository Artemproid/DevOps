Проект "Социальная сеть с чатом"
Пет-проект социальной сети с общим чатом и полным циклом контейнеризации и развёртывания.

Технологии
Backend: FastAPI, SQLAlchemy, SQLite, JWT-аутентификация

Frontend: React, React Router, React Bootstrap, Axios

DevOps / Инфраструктура:

Docker + Docker Compose — контейнеризация и оркестрация сервисов

Nginx — reverse proxy и раздача статики фронтенда

Multi-stage сборки Docker-образов для backend и frontend

Разделение окружений: dev / prod конфигурации

Управление секретами через env-переменные

Готовность к переходу на PostgreSQL для продакшена

Структура проекта
text
social-network/
├── backend/              # FastAPI-сервис
│   ├── app/              # Код приложения
│   ├── Dockerfile        # Multi-stage сборка backend
│   └── requirements.txt  # Зависимости Python
├── frontend/             # React SPA
│   ├── public/           # Статические файлы
│   ├── src/              # Исходный код
│   ├── Dockerfile        # Сборка и раздача через Nginx
│   └── package.json      # Зависимости NPM
├── nginx/                # Конфигурация reverse proxy
├── .env.example          # Шаблон переменных окружения
└── docker-compose.yml    # Оркестрация всех сервисов
DevOps-составляющая
Контейнеризация: каждый сервис (backend, frontend, nginx) изолирован в отдельном контейнере

Оркестрация: Docker Compose управляет сетью, томами и зависимостями между сервисами

Сеть: выделенная bridge-сеть для взаимодействия контейнеров

Reverse proxy: Nginx маршрутизирует запросы между фронтендом и API

Конфигурация: вынесена в env-файлы, секреты не попадают в репозиторий

Production-ready: multi-stage сборки, оптимизация образов, готовность к HTTPS и PostgreSQL

Запуск
bash
git clone <URL>
cd social-network
cp .env.example .env
docker-compose up -d --build
Приложение доступно по адресу: http://localhost:3000

Функциональность
Регистрация и авторизация (JWT)

Общий чат для всех пользователей

Просмотр сообщений в реальном времени

Направления развития инфраструктуры
Переход на PostgreSQL

Настройка CI/CD (Gitea + Drone / GitHub Actions)

Мониторинг через Prometheus + Grafana

Автоматизация деплоя и SSL через Let's Encrypt
