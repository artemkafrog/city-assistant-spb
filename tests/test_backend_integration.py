# tests/test_backend_integration.py
from config import get_config
from core.pipeline import CityAssistantPipeline
import asyncio
import pytest
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestBackendIntegration:
    """🧪 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ BACKEND-КОМПОНЕНТОВ"""

    @pytest.fixture
    async def pipeline(self):
        """Создание тестового пайплайна"""
        config = get_config('testing')
        pipeline = CityAssistantPipeline(config)
        await pipeline.initialize()
        yield pipeline
        # Cleanup можно добавить при необходимости

    @pytest.mark.asyncio
    async def test_pipeline_initialization(self, pipeline):
        """Тест инициализации пайплайна"""
        assert pipeline._initialized == True
        assert 'toxicity_filter' in pipeline.components
        assert 'dialog_manager' in pipeline.components
        assert 'vector_store' in pipeline.components
        assert 'llm_client' in pipeline.components

    @pytest.mark.asyncio
    async def test_user_query_processing(self, pipeline):
        """Тест обработки пользовательского запроса"""
        result = await pipeline.process_user_query(
            user_id="test_user_1",
            query="Как получить паспорт?"
        )

        assert result.status.value == "success"
        assert len(result.response) > 0
        assert result.processing_time > 0
        assert "паспорт" in result.response.lower()

    @pytest.mark.asyncio
    async def test_dialog_context_persistence(self, pipeline):
        """Тест сохранения контекста диалога"""
        user_id = "test_user_2"

        # Первый запрос
        result1 = await pipeline.process_user_query(user_id, "Привет")
        dialog1 = await pipeline.components['dialog_manager'].get_dialog_context(user_id)

        # Второй запрос
        result2 = await pipeline.process_user_query(user_id, "Как дела?")
        dialog2 = await pipeline.components['dialog_manager'].get_dialog_context(user_id)

        assert len(dialog2.messages) > len(dialog1.messages)
        assert dialog2.total_tokens > dialog1.total_tokens

    @pytest.mark.asyncio
    async def test_performance_benchmark(self, pipeline):
        """Тест производительности пайплайна"""
        import time

        start_time = time.time()
        queries = [
            "Как получить паспорт?",
            "Какие документы для субсидии?",
            "Как записаться к врачу?",
            "Где найти МФЦ?"
        ]

        results = []
        for query in queries:
            result = await pipeline.process_user_query(f"perf_user_{queries.index(query)}", query)
            results.append(result)

        total_time = time.time() - start_time
        avg_time = total_time / len(queries)

        print(f"⏱️  Среднее время обработки: {avg_time:.2f} секунд")

        # Проверяем что среднее время меньше 5 секунд (для mock-ов)
        assert avg_time < 5.0

        # Все запросы должны быть успешными
        assert all(r.status.value == "success" for r in results)


# Запуск тестов из командной строки
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
