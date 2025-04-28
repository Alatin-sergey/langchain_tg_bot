#!/usr/bin/make

all: update_env_file

update_env_file:
	python -c "import shutil; shutil.copyfile('./env.example', './.env')"

create_venv:
	python -m venv .venv

install_requirements: create_venv
	.venv/Scripts/python -m pip install -r requirements.txt

# Запуск сервисов
up_backend: update_env_file install_requirements
	python src/backend.py
	
up_frontend: update_env_file install_requirements
	python src/tg_bot.py


# Помощь
help:
	@echo "Доступные цели:"
	@echo "  up                 - Запуск сервисов"
	@echo "  update_env_file    - Обновление переменных окружения"

.PHONY: update_env_file up help create_venv install_requirements