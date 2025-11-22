# core/monitoring.py
"""
СИСТЕМА МОНИТОРИНГА И МЕТРИК
"""

import time
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import asyncio


@dataclass
class PipelineMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    toxic_blocks: int = 0
    average_response_time: float = 0.0
    last_request_time: datetime = None


class MetricsCollector:
    """
    Сбор и анализ метрик производительности системы
    """

    def __init__(self):
        self.metrics = PipelineMetrics()
        self._response_times: List[float] = []

    def record_request(self, success: bool, is_toxic: bool, response_time: float):
        """Запись метрик запроса"""
        self.metrics.total_requests += 1

        if is_toxic:
            self.metrics.toxic_blocks += 1
        elif success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1

        self._response_times.append(response_time)
        self.metrics.average_response_time = sum(
            self._response_times) / len(self._response_times)
        self.metrics.last_request_time = datetime.now()

        # Ограничение размера истории
        if len(self._response_times) > 1000:
            self._response_times = self._response_times[-1000:]

    def get_health_report(self) -> Dict:
        """Получение отчета о состоянии системы"""
        success_rate = (self.metrics.successful_requests /
                        self.metrics.total_requests * 100) if self.metrics.total_requests > 0 else 0

        return {
            'total_requests': self.metrics.total_requests,
            'success_rate': f"{success_rate:.1f}%",
            'average_response_time': f"{self.metrics.average_response_time:.2f}s",
            'toxic_blocks': self.metrics.toxic_blocks,
            'uptime': 'active'  # Можно добавить реальное время работы
        }
