class DialogManager:
    def add_message(self, user_id, role, content):
        """Учет контекста диалога (последние 5 сообщений)"""