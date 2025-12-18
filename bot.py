"""
Telegram Bot для CRM "СтройКонтроль"
Простая версия — только открытие Web App
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")

# Белый список Telegram ID
ALLOWED_USERS = [
    int(uid.strip()) 
    for uid in os.getenv("ALLOWED_USERS", "").split(",") 
    if uid.strip()
]


def is_authorized(user_id: int) -> bool:
    """Проверка авторизации по белому списку"""
    if not ALLOWED_USERS:
        return True  # Если список пуст — доступ всем
    return user_id in ALLOWED_USERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start"""
    user = update.effective_user
    
    if not is_authorized(user.id):
        await update.message.reply_text(
            f"⛔ Доступ запрещён.\n\nВаш ID: `{user.id}`",
            parse_mode="Markdown"
        )
        logger.warning(f"Unauthorized: {user.id} ({user.full_name})")
        return
    
    keyboard = [[
        InlineKeyboardButton(
            text="📋 Открыть CRM",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Нажми кнопку, чтобы открыть *СтройКонтроль*:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    logger.info(f"User: {user.id} ({user.full_name})")


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /myid"""
    await update.message.reply_text(
        f"🆔 Ваш ID: `{update.effective_user.id}`",
        parse_mode="Markdown"
    )


async def post_init(app: Application) -> None:
    """Установка кнопки меню"""
    if WEBAPP_URL:
        await app.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="📋 CRM",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )


def main():
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не указан в .env")
        return
    
    if not WEBAPP_URL:
        print("❌ Ошибка: WEBAPP_URL не указан в .env")
        return
    
    print(f"🚀 Запуск бота...")
    print(f"📎 Web App: {WEBAPP_URL}")
    
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
