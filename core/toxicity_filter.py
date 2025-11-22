# core/toxicity_filter.py
import asyncio
from typing import Dict, List, Tuple
from dataclasses import dataclass
import re
import logging

logger = logging.getLogger(__name__)

@dataclass
class ToxicityResult:
    is_toxic: bool
    confidence: float
    reason: str
    detected_patterns: List[str]
    safe_response: str = "Извините, я не могу ответить на это сообщение."

class ToxicityFilter:
    """
    🛡️ ФИЛЬТРАЦИЯ ТОКСИЧНЫХ И НЕПОДХОДЯЩИХ СООБЩЕНИЙ
    """
    
    def __init__(self, config):
        self.config = config
        self._patterns = self._compile_patterns()
        self._safe_responses = [
            "Извините, я не могу ответить на это сообщение.",
            "Давайте обсудим вопросы государственных услуг Санкт-Петербурга.",
            "Я здесь, чтобы помочь с официальной информацией о госуслугах.",
        ]
    
    async def analyze(self, text: str) -> ToxicityResult:
        """Анализ текста на токсичность"""
        text_lower = text.lower()
        
        # Проверка по регулярным выражениям
        pattern_matches = await self._check_patterns(text_lower)
        
        # Проверка по ключевым фразам
        phrase_matches = await self._check_toxic_phrases(text_lower)
        
        # Совокупная оценка
        all_matches = pattern_matches + phrase_matches
        is_toxic = len(all_matches) > 0
        confidence = min(1.0, len(all_matches) * 0.3)  # Простая эвристика
        
        return ToxicityResult(
            is_toxic=is_toxic,
            confidence=confidence,
            reason="Обнаружены недопустимые выражения" if is_toxic else "Текст безопасен",
            detected_patterns=all_matches,
            safe_response=self._get_safe_response()
        )
    
    async def _check_patterns(self, text: str) -> List[str]:
        """Проверка по регулярным выражениям"""
        matches = []
        for pattern_name, pattern in self._patterns.items():
            if pattern.search(text):
                matches.append(pattern_name)
        return matches
    
    async def _check_toxic_phrases(self, text: str) -> List[str]:
        """Проверка по списку токсичных фраз"""
        toxic_phrases = self.config.TOXICITY_FILTER_CONFIG.get('blocked_phrases', [])
        matches = []
        
        for phrase in toxic_phrases:
            if phrase in text:
                matches.append(f"фраза: {phrase}")
        
        return matches
    
    def _compile_patterns(self) -> Dict:
        """Компиляция регулярных выражений для обнаружения токсичности"""
        patterns = {
            'оскорбления': re.compile(r'\b(дурак|идиот|кретин|дебил|мудак)\b', re.IGNORECASE),
            'ненормативная_лексика': re.compile(r'\b([а-я]*х[а-я]*|бля|пизд)\w*\b', re.IGNORECASE),
            'угрозы': re.compile(r'\b(убью|зарежу|изобью|сожгу|разобью)\b', re.IGNORECASE),
            'экстремизм': re.compile(r'\b(терроризм|исламское государство|исламисты)\b', re.IGNORECASE),
        }
        return patterns
    
    def _get_safe_response(self) -> str:
        """Получение безопасного ответа"""
        import random
        return random.choice(self._safe_responses)