"""
Главный файл настроек для всех компонентов системы
Создан Backend-разработчиком для унификации и стандартизации проекта
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """
    🎯 КОНФИГУРАЦИЯ ВСЕЙ СИСТЕМЫ ГОРОДСКОГО ПОМОЩНИКА
    Централизованное хранилище всех настроек проекта
    """

    # =========================================================================
    # 🔐 БЕЗОПАСНОСТЬ И АУТЕНТИФИКАЦИЯ
    # =========================================================================

    # GigaChat API credentials - ОСНОВНОЙ API ДЛЯ AI
    GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS', '')
    GIGACHAT_SCOPE = os.getenv('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
    GIGACHAT_AUTH_URL = os.getenv(
        'GIGACHAT_AUTH_URL', 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth')
    GIGACHAT_API_URL = os.getenv(
        'GIGACHAT_API_URL', 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions')

    # Резервные AI провайдеры (для отказоустойчивости)
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # =========================================================================
    # 📁 СИСТЕМА ФАЙЛОВ И ПУТИ
    # =========================================================================

    # Корневая директория проекта
    PROJECT_ROOT = Path(__file__).parent.parent

    # Данные - RAW (сырые) и PROCESSED (обработанные)
    DATA_RAW_PATH = PROJECT_ROOT / 'data' / 'raw'
    DATA_PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed'
    DATA_EXTERNAL_PATH = PROJECT_ROOT / 'data' / 'external'

    # Векторная база данных ChromaDB
    CHROMA_DB_PATH = PROJECT_ROOT / 'chroma_db'
    CHROMA_COLLECTION_NAME = 'spb_knowledge_base'

    # Логи и мониторинг
    LOGS_PATH = PROJECT_ROOT / 'logs'
    METRICS_PATH = PROJECT_ROOT / 'metrics'

    # Кэш и временные файлы
    CACHE_PATH = PROJECT_ROOT / 'cache'
    TEMP_PATH = PROJECT_ROOT / 'temp'

    # =========================================================================
    # 🗃️ DATA ENGINEER НАСТРОЙКИ
    # =========================================================================

    # Источники данных для парсинга
    DATA_SOURCES = {
        'gu_spb_knowledge': {
            'url': 'https://gu.spb.ru/knowledge-base/',
            'enabled': True,
            'update_interval_hours': 24,
            'parser_timeout': 30
        },
        'gu_spb_mfc': {
            'url': 'https://gu.spb.ru/mfc/life_situations/',
            'enabled': True,
            'update_interval_hours': 24,
            'parser_timeout': 30
        },
        'spb_gov_services': {
            'url': 'https://www.gov.spb.ru/gov/otrasl/gtod/',
            'enabled': False,  # Резервный источник
            'update_interval_hours': 48,
            'parser_timeout': 30
        }
    }

    # Настройки парсинга
    PARSER_CONFIG = {
        'max_retries': 3,
        'retry_delay': 5,
        'request_timeout': 30,
        'user_agent': 'CityAssistantBot/1.0 (+https://github.com/spb-city-assistant)',
        'delay_between_requests': 1.0  # Анти-спам задержка
    }

    # =========================================================================
    # 🔍 RAG DEVELOPER НАСТРОЙКИ
    # =========================================================================

    # Настройки чанкинга (разбиения текстов)
    CHUNKING_CONFIG = {
        'chunk_size': 500,           # Размер чанка в символах
        'chunk_overlap': 50,         # Перекрытие между чанками
        # Приоритет разделителей
        'separators': ['\n\n', '\n', '. ', '! ', '? ', ' ', ''],
        'min_chunk_size': 100        # Минимальный размер чанка
    }

    # Модели для эмбеддингов
    EMBEDDING_CONFIG = {
        # Лучшая для русско-английских текстов
        'model_name': 'cointegrated/LaBSE-en-ru',
        'model_dimension': 768,                    # Размерность векторов
        'device': 'auto',                          # auto/cpu/cuda
        'batch_size': 32,                          # Размер батча для обработки
        'normalize_embeddings': True               # Нормализация векторов
    }

    # Настройки векторного поиска
    SEARCH_CONFIG = {
        'search_results_count': 4,           # Количество возвращаемых результатов
        'score_threshold': 0.7,              # Порог релевантности (0-1)
        # similarity/mmr (Maximal Marginal Relevance)
        'search_type': 'similarity',
        'mmr_diversity': 0.3,                # Параметр разнообразия для MMR
        'include_metadata': True             # Включать метаданные в результаты
    }

    # =========================================================================
    # 🤖 LLM INTEGRATION НАСТРОЙКИ
    # =========================================================================

    # Настройки GigaChat API
    GIGACHAT_CONFIG = {
        'model': 'GigaChat',                  # Модель для использования
        'temperature': 0.3,                   # Креативность (0-1)
        'max_tokens': 1024,                   # Максимальная длина ответа
        'top_p': 0.9,                         # Top-p sampling
        'repetition_penalty': 1.1,            # Штраф за повторения
        'request_timeout': 60,                # Таймаут запроса в секундах
        'max_retries': 3,                     # Максимальное количество повторов
        'retry_delay': 2                      # Задержка между повторами
    }

    # Промт-шаблоны для разных типов запросов
    PROMPT_TEMPLATES = {
        'city_assistant': """
Ты - вежливый и компетентный помощник по вопросам государственных услуг Санкт-Петербурга.
Отвечай ТОЛЬКО на основе предоставленного контекста. Если в контексте нет информации - честно говори "Не знаю".

КОНТЕКСТ ДЛЯ ОТВЕТА:
{context}

ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}

ИСТОРИЯ ДИАЛОГА:
{history}

ОТВЕТАЙ НА РУССКОМ ЯЗЫКЕ:
- Будь точным и конкретным
- Ссылайся на официальные источники
- Если нужно несколько шагов - перечисли их по порядку
- Указывай необходимые документы и сроки
- Сохраняй дружелюбный и профессиональный тон
"""
    }

    # =========================================================================
    # ⚙️ BACKEND DEVELOPER НАСТРОЙКИ
    # =========================================================================

    # Настройки основного пайплайна
    PIPELINE_CONFIG = {
        'max_response_time': 30,              # Максимальное время ответа в секундах
        'enable_toxicity_filter': True,       # Включить фильтр токсичности
        'enable_dialog_context': True,        # Включить контекст диалога
        'fallback_to_basic_search': True,     # Резервный режим при ошибках AI
        'cache_responses': True,              # Кэшировать ответы
        'cache_ttl_minutes': 60               # Время жизни кэша
    }

    # Настройки фильтра токсичности
    TOXICITY_FILTER_CONFIG = {
        'enabled': True,
        'model_name': 'cointegrated/rubert-tiny-toxicity',
        'threshold': 0.8,                     # Порог токсичности (0-1)
        'blocked_phrases': [                  # Список блокируемых фраз
            'терроризм', 'экстремизм', 'наркотики', 'оскорбление'
        ]
    }

    # Настройки управления диалогом
    DIALOG_MANAGER_CONFIG = {
        'max_history_messages': 6,            # Максимальная история диалога
        'context_window_tokens': 2000,        # Максимальное количество токенов контекста
        # Профилирование пользователей (выкл для приватности)
        'enable_user_profiling': False,
        'session_timeout_minutes': 30         # Таймаут сессии
    }

    # Настройки кэширования
    CACHE_CONFIG = {
        'enabled': True,
        'backend': 'disk',                    # disk/redis/memory
        'ttl_hours': 24,                      # Время жизни кэша
        'max_size_mb': 100                    # Максимальный размер кэша
    }

    # =========================================================================
    # 🎨 FRONTEND DEVELOPER НАСТРОЙКИ
    # =========================================================================

    # Настройки Streamlit приложения
    STREAMLIT_CONFIG = {
        'page_title': "Санкт-Петербург - Городской помощник",
        'page_icon': "🏙️",
        'layout': "centered",
        'initial_sidebar_state': "expanded",
        'theme': {
            'primaryColor': '#1E88E5',
            'backgroundColor': '#FFFFFF',
            'secondaryBackgroundColor': '#F5F5F5',
            'textColor': '#262730',
            'font': 'sans serif'
        }
    }

    # UI/UX настройки
    UI_CONFIG = {
        'max_message_length': 2000,           # Максимальная длина сообщения
        'typing_animation_delay': 0.02,       # Задержка анимации печати
        # Голосовой ввод (задел на будущее)
        'enable_voice_input': False,
        # Загрузка файлов (задел на будущее)
        'enable_file_upload': False,
        # Предупреждение о долгом ответе (сек)
        'response_time_warning': 15
    }

    # =========================================================================
    # 📊 МОНИТОРИНГ И ЛОГИРОВАНИЕ
    # =========================================================================

    # Настройки логирования
    LOGGING_CONFIG = {
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'date_format': '%Y-%m-%d %H:%M:%S',
        'max_file_size_mb': 10,
        'backup_count': 5
    }

    # Метрики и аналитика
    METRICS_CONFIG = {
        'enable_metrics': True,
        'track_response_times': True,
        'track_user_questions': True,
        'track_system_errors': True,
        'anonymize_user_data': True           # Анонимизация данных пользователей
    }

    # =========================================================================
    # 🚀 ДЕПЛОЙ И ПРОИЗВОДИТЕЛЬНОСТЬ
    # =========================================================================

    # Настройки производительности
    PERFORMANCE_CONFIG = {
        'max_concurrent_requests': 10,        # Максимум одновременных запросов
        'database_connection_timeout': 10,    # Таймаут подключения к БД
        'enable_compression': True,           # Сжатие данных
        'background_tasks_workers': 2         # Количество воркеров фоновых задач
    }

    # Настройки деплоя
    DEPLOYMENT_CONFIG = {
        # development/staging/production
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        'host': os.getenv('HOST', '0.0.0.0'),
        'port': int(os.getenv('PORT', 8501)),
        'reload': os.getenv('RELOAD', 'False').lower() == 'true'
    }


class DevelopmentConfig(Config):
    """Конфигурация для режима разработки"""

    def __init__(self):
        super().__init__()
        self.DEPLOYMENT_CONFIG['debug'] = True
        self.DEPLOYMENT_CONFIG['reload'] = True
        self.LOGGING_CONFIG['level'] = logging.DEBUG
        # Больше времени для дебага
        self.PIPELINE_CONFIG['max_response_time'] = 60


class ProductionConfig(Config):
    """Конфигурация для продакшена"""

    def __init__(self):
        super().__init__()
        self.DEPLOYMENT_CONFIG['debug'] = False
        self.DEPLOYMENT_CONFIG['reload'] = False
        self.LOGGING_CONFIG['level'] = logging.WARNING
        self.PERFORMANCE_CONFIG['max_concurrent_requests'] = 50
        self.GIGACHAT_CONFIG['max_retries'] = 5


class TestingConfig(Config):
    """Конфигурация для тестирования"""

    def __init__(self):
        super().__init__()
        self.DEPLOYMENT_CONFIG['debug'] = True
        self.GIGACHAT_CREDENTIALS = 'TEST_CREDENTIALS'
        self.PIPELINE_CONFIG['enable_toxicity_filter'] = False
        self.CACHE_CONFIG['enabled'] = False


def get_config(environment=None):
    """
    Фабрика конфигураций - возвращает нужную конфигурацию по окружению
    """
    env = environment or os.getenv('ENVIRONMENT', 'development')

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    config_class = config_map.get(env, Config)
    return config_class()


def initialize_directories(config):
    """
    Инициализация всех необходимых директорий проекта
    """
    directories = [
        config.DATA_RAW_PATH,
        config.DATA_PROCESSED_PATH,
        config.DATA_EXTERNAL_PATH,
        config.CHROMA_DB_PATH,
        config.LOGS_PATH,
        config.METRICS_PATH,
        config.CACHE_PATH,
        config.TEMP_PATH
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Создана директория: {directory}")


def setup_logging(config):
    """
    Настройка системы логирования
    """
    logging.basicConfig(
        level=config.LOGGING_CONFIG['level'],
        format=config.LOGGING_CONFIG['format'],
        datefmt=config.LOGGING_CONFIG['date_format'],
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.LOGS_PATH / 'city_assistant.log')
        ]
    )

    # Уменьшаем логирование для сторонних библиотек
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('chromadb').setLevel(logging.WARNING)


# Глобальная инициализация при импорте
config = get_config()
initialize_directories(config)
setup_logging(config)

# Создаем логгер для этого модуля
logger = logging.getLogger(__name__)
logger.info("🎯 Конфигурация City Assistant успешно загружена!")

if __name__ == "__main__":
    # Тестовый вывод конфигурации
    print("=" * 50)
    print("🏙️ КОНФИГУРАЦИЯ ГОРОДСКОГО ПОМОЩНИКА")
    print("=" * 50)

    print(
        f"🔐 GigaChat настроен: {'✅' if config.GIGACHAT_CREDENTIALS else '❌'}")
    print(f"📁 Данные: {config.DATA_RAW_PATH}")
    print(f"🔍 Векторная БД: {config.CHROMA_DB_PATH}")
    print(f"🌍 Окружение: {config.DEPLOYMENT_CONFIG['environment']}")
    print(f"🐛 Debug режим: {config.DEPLOYMENT_CONFIG['debug']}")

    print("\n📊 Источники данных:")
    for source_name, source_config in config.DATA_SOURCES.items():
        status = '✅' if source_config['enabled'] else '❌'
        print(f"  {status} {source_name}: {source_config['url']}")

    print("=" * 50)
