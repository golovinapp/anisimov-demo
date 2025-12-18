@echo off
chcp 65001 >nul

if not exist .env (
    copy .env.example .env
    echo Создан .env — заполни и запусти снова
    pause
    exit /b 1
)

if not exist venv python -m venv venv
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
python bot.py
pause
