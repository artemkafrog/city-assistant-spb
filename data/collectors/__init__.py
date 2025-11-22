# data/collectors/__init__.py
from .base_collector import BaseDataCollector
from .gu_spb_collector import GUSpbCollector
from .mfc_collector import MFCCollector

# Теперь можно писать:
# from data.collectors import BaseDataCollector

__all__ = ['BaseDataCollector', 'GUSpbCollector', 'MFCCollector']