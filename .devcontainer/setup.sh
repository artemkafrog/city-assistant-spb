#!/bin/bash

echo "🚀 Настройка среды разработки City Assistant..."

# Обновление пакетов
sudo apt-get update

# Создание структуры папок
mkdir -p data/raw data/processed chroma_db logs tests/unit tests/integration

# Установка Python зависимостей
echo "📦 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Установка предобученных моделей для NLP
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
print('✅ NLP модели установлены')
"

# Настройка git hooks
echo "🔧 Настройка git hooks..."
cp scripts/git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Создание тестовых данных
python scripts/create_sample_data.py

echo "🎉 Среда разработки готова!"
echo "👉 Запустите проект: streamlit run app.py"