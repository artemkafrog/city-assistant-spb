from .base_collector import BaseDataCollector # Импорт из base_collector.py

class GUSpbCollector(BaseDataCollector):
    def collect_data(self):
        """Парсинг с https://gu.spb.ru/knowledge-base/"""
        # TODO: Собрать информацию о госуслугах