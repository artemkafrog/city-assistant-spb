import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    # GigaChat
    GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS', '')
    
    # Пути к данным
    DATA_RAW_PATH = 'data/raw'
    DATA_PROCESSED_PATH = 'data/processed'
    CHROMA_DB_PATH = 'chroma_db'
    LOGS_PATH = 'logs'
    
    # Настройки RAG
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    SEARCH_RESULTS_COUNT = 4
    
    # Настройки модели
    EMBEDDING_MODEL = 'cointegrated/LaBSE-en-ru'
    
    # Настройки приложения
    MAX_HISTORY_MESSAGES = 6
    REQUEST_TIMEOUT = 30

# Создаем папки при импорте
for path in [Config.DATA_RAW_PATH, Config.DATA_PROCESSED_PATH, 
             Config.CHROMA_DB_PATH, Config.LOGS_PATH]:
    os.makedirs(path, exist_ok=True)