# СтройКонтроль — Telegram CRM Bot

## Быстрый старт

### 1. Создайте бота в Telegram

1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Скопируйте токен

### 2. Настройте окружение

```bash
# Скопируйте пример конфига
cp .env.example .env

# Отредактируйте .env
nano .env
```

Заполните:
- `BOT_TOKEN` — токен от BotFather
- `WEBAPP_URL` — публичный HTTPS URL вашего сервера
- `ALLOWED_USERS` — Telegram ID разрешённых пользователей

### 3. Запустите

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```
start.bat
```

## Настройка HTTPS (обязательно для Web App)

### Вариант A: Nginx + Let's Encrypt

```nginx
server {
    listen 443 ssl http2;
    server_name crm.example.com;

    ssl_certificate /etc/letsencrypt/live/crm.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/crm.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Вариант B: Cloudflare Tunnel (без белого IP)

```bash
cloudflared tunnel --url http://localhost:8080
```

## Структура проекта

```
anisimov-demo/
├── bot.py              # Основной код бота
├── html/
│   └── index.html      # Web App интерфейс
├── requirements.txt    # Python зависимости
├── .env.example        # Пример конфигурации
├── .env                # Ваша конфигурация (не в git!)
├── start.sh            # Скрипт запуска Linux
└── start.bat           # Скрипт запуска Windows
```

## Команды бота

- `/start` — Открыть CRM
- `/help` — Справка
- `/myid` — Узнать свой Telegram ID

## Добавление пользователей

1. Попросите пользователя отправить `/myid` боту
2. Добавьте его ID в `ALLOWED_USERS` в `.env`
3. Перезапустите бота

## Troubleshooting

**Web App не открывается:**
- Проверьте что `WEBAPP_URL` начинается с `https://`
- Убедитесь что сертификат валидный

**Бот не отвечает:**
- Проверьте `BOT_TOKEN` в `.env`
- Посмотрите логи: `python bot.py`

**Ошибка доступа:**
- Проверьте свой ID через `/myid`
- Добавьте ID в `ALLOWED_USERS`
