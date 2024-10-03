#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python3 не найден. Пожалуйста, установите Python3 перед запуском этого скрипта."
    exit 1
fi

python3 -m venv .venv

pip install --upgrade pip

pip install --upgrade typing-extensions
pip install dict2xml
pip install connexion[flask] connexion[swagger-ui] connexion[uvicorn]
pip install flask-restplus
pip install Flask

echo "Установка зависимостей завершена. Виртуальное окружение активировано."
