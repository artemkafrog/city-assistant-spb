class CityAssistantPipeline:
    def process_query(self, user_question):
        """Основной пайплайн обработки запроса:
        1. Проверка токсичности
        2. Поиск в векторной БД
        3. Формирование промта
        4. Запрос к GigaChat
        5. Возврат ответа
        """