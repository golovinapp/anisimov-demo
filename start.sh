#!/bin/bash
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Создан .env — заполни и запусти снова"
    exit 1
fi

[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python bot.py
