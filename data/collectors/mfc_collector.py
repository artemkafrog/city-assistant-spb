from .base_collector import BaseDataCollector # Импорт из base_collector.py

class MFCCollector(BaseDataCollector):
    def collect_data(self):
        """Парсинг с https://gu.spb.ru/mfc/life_situations"""
        