# core/pipeline.py
import asyncio
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PipelineStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    TOXIC_DETECTED = "toxic_detected"
    TIMEOUT = "timeout"


@dataclass
class PipelineResult:
    status: PipelineStatus
    response: str
    context_used: List[str]
    processing_time: float
    error_message: Optional[str] = None
    metadata: Dict = None


class CityAssistantPipeline:
    """
    🎯 ОСНОВНОЙ ПАЙПЛАЙН ОБРАБОТКИ ЗАПРОСОВ
    Координирует работу всех компонентов системы
    """

    def __init__(self, config):
        self.config = config
        self._initialized = False
        self.components = {}

    async def initialize(self):
        """Асинхронная инициализация всех компонентов"""
        logger.info("🔄 Инициализация пайплайна...")

        # Инициализация компонентов в правильном порядке
        init_sequence = [
            self._init_toxicity_filter,
            self._init_dialog_manager,
            self._init_vector_store,
            self._init_llm_client
        ]

        for init_func in init_sequence:
            try:
                await init_func()
            except Exception as e:
                logger.error(
                    f"❌ Ошибка инициализации {init_func.__name__}: {e}")
                raise

        self._initialized = True
        logger.info("✅ Пайплайн успешно инициализирован")

    async def _init_toxicity_filter(self):
        """Инициализация фильтра токсичности"""
        # Временная заглушка - потом заменится на реальную модель
        self.components['toxicity_filter'] = MockToxicityFilter(self.config)
        logger.debug("✅ Фильтр токсичности инициализирован")

    async def _init_dialog_manager(self):
        """Инициализация менеджера диалога"""
        self.components['dialog_manager'] = DialogManager(self.config)
        logger.debug("✅ Менеджер диалога инициализирован")

    async def _init_vector_store(self):
        """Инициализация векторного хранилища"""
        # Заглушка для RAG разработчика
        self.components['vector_store'] = MockVectorStore(self.config)
        logger.debug("✅ Векторное хранилище инициализировано")

    async def _init_llm_client(self):
        """Инициализация LLM клиента"""
        # Заглушка для LLM разработчика
        self.components['llm_client'] = MockLLMClient(self.config)
        logger.debug("✅ LLM клиент инициализирован")

    async def process_user_query(self, user_id: str, query: str) -> PipelineResult:
        """
        Основной метод обработки пользовательского запроса
        """
        if not self._initialized:
            raise RuntimeError(
                "Пайплайн не инициализирован. Вызовите initialize()")

        start_time = time.time()

        try:
            # 1. ✅ ПРОВЕРКА ТОКСИЧНОСТИ
            toxicity_result = await self._check_toxicity(query)
            if toxicity_result.is_toxic:
                return PipelineResult(
                    status=PipelineStatus.TOXIC_DETECTED,
                    response=toxicity_result.safe_response,
                    context_used=[],
                    processing_time=time.time() - start_time,
                    metadata={'toxicity_reason': toxicity_result.reason}
                )

            # 2. 📝 ОБНОВЛЕНИЕ КОНТЕКСТА ДИАЛОГА
            dialog_context = await self._update_dialog_context(user_id, query)

            # 3. 🔍 ПОИСК РЕЛЕВАНТНОЙ ИНФОРМАЦИИ
            search_results = await self._search_relevant_info(query, dialog_context)

            # 4. 🤖 ГЕНЕРАЦИЯ ОТВЕТА С ПОМОЩЬЮ LLM
            llm_response = await self._generate_llm_response(
                query, search_results, dialog_context
            )

            # 5. 💾 СОХРАНЕНИЕ ОТВЕТА В ИСТОРИЮ
            await self._save_to_history(user_id, "assistant", llm_response.response)

            return PipelineResult(
                status=PipelineStatus.SUCCESS,
                response=llm_response.response,
                context_used=search_results.used_documents,
                processing_time=time.time() - start_time,
                metadata={
                    'llm_metadata': llm_response.metadata,
                    'search_metadata': search_results.metadata
                }
            )

        except asyncio.TimeoutError:
            logger.warning(
                f"⏰ Таймаут обработки запроса от пользователя {user_id}")
            return PipelineResult(
                status=PipelineStatus.TIMEOUT,
                response="Извините, обработка запроса заняла слишком много времени. Попробуйте позже.",
                context_used=[],
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"❌ Ошибка обработки запроса: {e}")
            return PipelineResult(
                status=PipelineStatus.ERROR,
                response="Произошла внутренняя ошибка. Пожалуйста, попробуйте еще раз.",
                context_used=[],
                processing_time=time.time() - start_time,
                error_message=str(e)
            )

    async def _check_toxicity(self, text: str):
        """Проверка текста на токсичность"""
        return await self.components['toxicity_filter'].analyze(text)

    async def _update_dialog_context(self, user_id: str, query: str):
        """Обновление контекста диалога"""
        return await self.components['dialog_manager'].add_user_message(user_id, query)

    async def _search_relevant_info(self, query: str, context):
        """Поиск релевантной информации"""
        return await self.components['vector_store'].search(query, context)

    async def _generate_llm_response(self, query: str, search_results, context):
        """Генерация ответа с помощью LLM"""
        return await self.components['llm_client'].generate_response(
            query, search_results, context
        )

    async def _save_to_history(self, user_id: str, role: str, message: str):
        """Сохранение сообщения в историю"""
        await self.components['dialog_manager'].add_message(user_id, role, message)
