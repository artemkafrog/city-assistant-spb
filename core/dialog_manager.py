# core/dialog_manager.py
import json
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class DialogMessage:
    role: str  # 'user' | 'assistant'
    content: str
    timestamp: datetime
    tokens: int = 0

@dataclass  
class DialogContext:
    user_id: str
    messages: List[DialogMessage]
    total_tokens: int
    created_at: datetime
    updated_at: datetime

class DialogManager:
    """
    🧠 УПРАВЛЕНИЕ КОНТЕКСТОМ ДИАЛОГА И ИСТОРИЕЙ СООБЩЕНИЙ
    """
    
    def __init__(self, config):
        self.config = config
        self._dialogs: Dict[str, DialogContext] = {}
        self._cleanup_task = None
        
    async def start_cleanup_task(self):
        """Запуск фоновой задачи очистки устаревших диалогов"""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
    
    async def add_user_message(self, user_id: str, message: str) -> DialogContext:
        """Добавление сообщения пользователя и возврат обновленного контекста"""
        dialog = await self._get_or_create_dialog(user_id)
        
        user_msg = DialogMessage(
            role='user',
            content=message,
            timestamp=datetime.now(),
            tokens=self._estimate_tokens(message)
        )
        
        dialog.messages.append(user_msg)
        dialog.total_tokens += user_msg.tokens
        dialog.updated_at = datetime.now()
        
        # Обрезка истории если превышен лимит
        await self._trim_dialog_history(dialog)
        
        logger.debug(f"💬 Добавлено сообщение пользователя {user_id}, токенов: {dialog.total_tokens}")
        return dialog
    
    async def add_message(self, user_id: str, role: str, message: str):
        """Добавление любого сообщения в диалог"""
        dialog = await self._get_or_create_dialog(user_id)
        
        msg = DialogMessage(
            role=role,
            content=message,
            timestamp=datetime.now(),
            tokens=self._estimate_tokens(message)
        )
        
        dialog.messages.append(msg)
        dialog.total_tokens += msg.tokens
        dialog.updated_at = datetime.now()
        
        await self._trim_dialog_history(dialog)
    
    async def get_dialog_context(self, user_id: str) -> Optional[DialogContext]:
        """Получение текущего контекста диалога"""
        return self._dialogs.get(user_id)
    
    async def clear_dialog(self, user_id: str):
        """Очистка диалога пользователя"""
        if user_id in self._dialogs:
            del self._dialogs[user_id]
            logger.info(f"🧹 Диалог пользователя {user_id} очищен")
    
    async def _get_or_create_dialog(self, user_id: str) -> DialogContext:
        """Получение или создание нового диалога"""
        if user_id not in self._dialogs:
            self._dialogs[user_id] = DialogContext(
                user_id=user_id,
                messages=[],
                total_tokens=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            logger.debug(f"🆕 Создан новый диалог для пользователя {user_id}")
        
        return self._dialogs[user_id]
    
    async def _trim_dialog_history(self, dialog: DialogContext):
        """Обрезка истории диалога если превышены лимиты"""
        max_messages = self.config.DIALOG_MANAGER_CONFIG['max_history_messages']
        max_tokens = self.config.DIALOG_MANAGER_CONFIG['context_window_tokens']
        
        # Обрезка по количеству сообщений
        while len(dialog.messages) > max_messages:
            removed_msg = dialog.messages.pop(0)
            dialog.total_tokens -= removed_msg.tokens
        
        # Обрезка по количеству токенов
        while dialog.total_tokens > max_tokens and len(dialog.messages) > 1:
            removed_msg = dialog.messages.pop(0)
            dialog.total_tokens -= removed_msg.tokens
    
    def _estimate_tokens(self, text: str) -> int:
        """Примерная оценка количества токенов в тексте"""
        # Упрощенная оценка: 1 токен ≈ 4 символа для русского языка
        return max(1, len(text) // 4)
    
    async def _periodic_cleanup(self):
        """Периодическая очистка устаревших диалогов"""
        while True:
            try:
                await asyncio.sleep(300)  # Каждые 5 минут
                await self._cleanup_old_dialogs()
            except Exception as e:
                logger.error(f"❌ Ошибка в cleanup task: {e}")
    
    async def _cleanup_old_dialogs(self):
        """Очистка диалогов старше timeout"""
        timeout_minutes = self.config.DIALOG_MANAGER_CONFIG['session_timeout_minutes']
        cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
        
        expired_users = [
            user_id for user_id, dialog in self._dialogs.items()
            if dialog.updated_at < cutoff_time
        ]
        
        for user_id in expired_users:
            await self.clear_dialog(user_id)
        
        if expired_users:
            logger.info(f"🧹 Очищено {len(expired_users)} устаревших диалогов")