# core/mocks.py
"""
ЗАГЛУШКИ ДЛЯ КОМПОНЕНТОВ, КОТОРЫЕ ЕЩЕ РАЗРАБАТЫВАЮТСЯ
"""

import asyncio
import random
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class MockSearchResult:
    documents: List[str]
    metadatas: List[Dict]
    distances: List[float]
    used_documents: List[str]
    metadata: Dict


@dataclass
class MockLLMResponse:
    response: str
    metadata: Dict


class MockToxicityFilter:
    def __init__(self, config):
        self.config = config

    async def analyze(self, text: str):
        # Заглушка - всегда возвращает безопасный текст
        from core.toxicity_filter import ToxicityResult
        return ToxicityResult(
            is_toxic=False,
            confidence=0.0,
            reason="Текст безопасен",
            detected_patterns=[]
        )


class MockVectorStore:
    def __init__(self, config):
        self.config = config
        self._mock_documents = self._create_mock_documents()

    async def search(self, query: str, context, n_results: int = 4):
        # Имитация поиска по запросу
        await asyncio.sleep(0.1)  # Имитация задержки

        # Простая логика "поиска" на основе ключевых слов
        query_lower = query.lower()
        relevant_docs = []

        for doc in self._mock_documents:
            if any(keyword in query_lower for keyword in doc['keywords']):
                relevant_docs.append(doc)

        # Если не нашли релевантных, берем случайные
        if not relevant_docs:
            relevant_docs = random.sample(self._mock_documents, min(
                n_results, len(self._mock_documents)))
        else:
            relevant_docs = relevant_docs[:n_results]

        return MockSearchResult(
            documents=[doc['content'] for doc in relevant_docs],
            metadatas=[doc['metadata'] for doc in relevant_docs],
            distances=[random.uniform(0.1, 0.5) for _ in relevant_docs],
            used_documents=[doc['metadata']['source']
                            for doc in relevant_docs],
            metadata={'search_strategy': 'mock', 'query_processed': query}
        )

    def _create_mock_documents(self):
        """Создание mock-документов для тестирования"""
        return [
            {
                'content': 'Для получения паспорта РФ обратитесь в МФЦ с заявлением и документами: свидетельство о рождении, фото 3x4.',
                'keywords': ['паспорт', 'документы', 'мфц', 'получить'],
                'metadata': {'source': 'gu_spb', 'type': 'passport_info'}
            },
            {
                'content': 'Субсидия на ЖКХ предоставляется при доходе ниже прожиточного минимума. Необходимы справки о доходах.',
                'keywords': ['субсидия', 'жкх', 'доход', 'справка'],
                'metadata': {'source': 'gu_spb', 'type': 'subsidy_info'}
            }
        ]


class MockLLMClient:
    def __init__(self, config):
        self.config = config

    async def generate_response(self, query: str, search_results, context):
        await asyncio.sleep(0.5)  # Имитация работы LLM

        # Простая логика генерации ответа на основе запроса
        responses = {
            'паспорт': 'Для получения паспорта обратитесь в ближайший МФЦ с документами.',
            'субсидия': 'Информация о субсидиях на ЖКХ доступна на портале госуслуг.',
            'default': 'Я помогу вам с вопросами государственных услуг Санкт-Петербурга.'
        }

        query_lower = query.lower()
        response_text = responses['default']

        for key, response in responses.items():
            if key in query_lower and key != 'default':
                response_text = response
                break

        return MockLLMResponse(
            response=response_text,
            metadata={'model': 'mock', 'tokens_used': 50}
        )
