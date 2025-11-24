import os
import requests
import json
from typing import Optional
from config import Config

class GigaChatClient:
    def __init__(self, credentials: Optional[str] = None):
        """
        Инициализация клиента GigaChat API
        
        ВХОД:
        - credentials: учетные данные GigaChat (логин:пароль или токен)
        
        ВЫХОД: настроенный клиент для работы с API
        """
        self.credentials = credentials or Config.GIGACHAT_CREDENTIALS
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires = 0
        
        if not self.credentials:
            raise ValueError("Не указаны учетные данные GigaChat. Установите GIGACHAT_CREDENTIALS в config.py")
        
        print("🔑 Инициализация GigaChat клиента...")
        self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в GigaChat API"""
        try:
            # Для логина/пароля
            auth_response = requests.post(
                f"{self.base_url}/oauth",
                headers={
                    "Authorization": f"Bearer {self.credentials}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data="scope=GIGACHAT_API_PERS",
                verify=False  # Отключаем проверку SSL для тестирования
            )
            
            if auth_response.status_code == 200:
                token_data = auth_response.json()
                self.access_token = token_data.get("access_token")
                self.token_expires = token_data.get("expires_at", 0)
                print("✅ Успешная аутентификация в GigaChat")
            else:
                raise Exception(f"Ошибка аутентификации: {auth_response.status_code} - {auth_response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка аутентификации: {e}")
            # Fallback: используем credentials как access token
            self.access_token = self.credentials
            print("⚠️ Используются credentials как access token")
    
    def _ensure_valid_token(self):
        """Проверка и обновление токена при необходимости"""
        # TODO: Добавить логику обновления токена
        pass
    
    def get_response(self, prompt: str, temperature: float = 0.3, max_tokens: int = 1500) -> str:
        """
        Отправка запроса к GigaChat и получение ответа
        
        ВХОД:
        - prompt: готовый промт для отправки
        - temperature: креативность ответа (0.1-1.0)
        - max_tokens: максимальная длина ответа
        
        ВЫХОД: текстовый ответ от GigaChat
        """
        try:
            self._ensure_valid_token()
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "GigaChat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_msg = f"Ошибка API: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return f"Извините, произошла ошибка при обращении к сервису. Пожалуйста, попробуйте позже."
                
        except requests.exceptions.Timeout:
            return "Извините, сервис временно недоступен. Пожалуйста, попробуйте позже."
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return "Извините, произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз."