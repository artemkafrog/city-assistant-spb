import streamlit as st
import time
from datetime import datetime
import pytz
import json
import os

# =============================================================================
# БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
# =============================================================================
# from core.pipeline import CityAssistantPipeline
# from search.vector_store import VectorStore
# from llm.gigachat_client import GigaChatClient
# from core.toxicity_filter import ToxicityFilter
# from data.collectors.gu_spb_collector import GUSpbCollector
# =============================================================================

st.set_page_config(page_title="City Assistant — Chat", layout="wide")

# --- Styles: message bubbles, avatars, layout ---
st.markdown(
    """
    <style>
    .chat-container { max-width: 900px; margin: 0 auto; }
    .msg-row { display:flex; gap:10px; margin-bottom:10px; align-items:flex-end; }
    .msg-row.user { justify-content:flex-end; }
    .avatar { width:40px; height:40px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:bold; }
    .bubble { max-width:70%; padding:12px 16px; border-radius:18px; line-height:1.3; }
    .bubble.user { background:#0b93f6; color:white; border-bottom-right-radius:4px; }
    .bubble.assistant { background:#f1f0f0; color:#111; border-bottom-left-radius:4px; }
    .meta { font-size:11px; color:#888; margin-top:4px; }
    .typing { font-style:italic; color:#666; margin-left:6px; }
    
    /* responsive */
    @media (max-width:600px) {
      .bubble { max-width:85%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Mock Backend Integration ---
class MockCityAssistant:
    """Временная заглушка для бэкенда, пока компоненты не готовы"""
    
    def __init__(self):
        # =============================================================================
        # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
        # =============================================================================
        # self.pipeline = CityAssistantPipeline()
        # self.vector_store = VectorStore()
        # self.llm_client = GigaChatClient()
        # self.toxicity_filter = ToxicityFilter()
        # =============================================================================
        pass
    
    def process_query(self, user_input, chat_history=None):
        """Обрабатывает запрос пользователя и возвращает ответ"""
        
        # =============================================================================
        # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
        # =============================================================================
        # # Проверка на токсичность
        # is_toxic, reason = self.toxicity_filter.is_toxic(user_input)
        # if is_toxic:
        #     return f"Извините, но я не могу ответить на этот вопрос. {reason}"
        # 
        # # Поиск релевантной информации
        # search_results = self.vector_store.search(user_input, n_results=3)
        # 
        # # Генерация ответа через LLM
        # response = self.llm_client.get_city_assistant_response(
        #     question=user_input,
        #     context=search_results['documents'],
        #     chat_history=chat_history
        # )
        # 
        # return response
        # =============================================================================
        
        # Временная логика ответов на основе ключевых слов
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['паспорт', 'документ']):
            return "Для получения паспорта обратитесь в МФЦ с документами: заявление, фото 3x4, квитанция об оплате госпошлины. Срок изготовления - 10 дней."
        
        elif any(word in user_input_lower for word in ['субсиди', 'жкх', 'коммунал']):
            return "Субсидия на ЖКХ предоставляется при превышении 22% дохода на коммунальные услуги. Обратитесь в МФЦ со справками о доходах и документами на жилье."
        
        elif any(word in user_input_lower for word in ['мфц', 'многофункциональный']):
            return "МФЦ (Многофункциональный центр) предоставляет государственные и муниципальные услуги. Режим работы: пн-пт 9:00-20:00, сб 10:00-17:00. Запись через портал госуслуг."
        
        elif any(word in user_input_lower for word in ['детск', 'сад', 'очеред']):
            return "Для записи в детский сад подайте заявление через портал госуслуг или МФЦ. Потребуется свидетельство о рождении ребенка и документы родителей."
        
        elif any(word in user_input_lower for word in ['эрмитаж', 'музей', 'достопримечательность']):
            return "Эрмитаж работает с 10:30 до 18:00 (вторник-воскресенье). Стоимость билета: 500 руб. Адрес: Дворцовая пл., 2. Бесплатный вход - третий четверг месяца."
        
        elif any(word in user_input_lower for word in ['метро', 'проезд', 'транспорт']):
            return "Метро Санкт-Петербурга работает с 5:30 до 00:30. Стоимость проезда: 70 руб. Есть проездные на 1-90 дней. Основные станции пересадок: Площадь Восстания, Технологический институт."
        
        else:
            return f"Я получил ваш вопрос: '{user_input}'. Как городской помощник, я могу предоставить информацию о госуслугах, достопримечательностях, транспорте и других городских услугах Санкт-Петербурга."

# --- Helpers ---
def get_local_time():
    """Получаем локальное время с учетом часового пояса"""
    try:
        local_tz = pytz.timezone('Europe/Moscow')
        local_time = datetime.now(local_tz)
        return local_time.strftime("%H:%M")
    except:
        return datetime.now().strftime("%H:%M")

def _default_history():
    return [
        {"role": "assistant", "text": "Привет! Я City Assistant. Чем могу помочь с вопросами о Санкт-Петербурге?",
            "time": get_local_time()},
    ]

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = _default_history()

if "assistant" not in st.session_state:
    # =============================================================================
    # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
    # =============================================================================
    # st.session_state.assistant = CityAssistantPipeline()
    # =============================================================================
    st.session_state.assistant = MockCityAssistant()

# Функция для рендера сообщений
def render_messages():
    for m in st.session_state.get("messages", []):
        if m["role"] == "user":
            with st.container():
                st.markdown(
                    f"<div class='msg-row user'><div class='bubble user'>{m['text']}</div><div class='avatar' style='background:#0b93f6;color:white;'>U</div></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='meta' style='text-align:right;'>{m['time']}</div>", unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(
                    f"<div class='msg-row'><div class='avatar' style='background:#e0e0e0;color:#333;'>A</div><div class='bubble assistant'>{m['text']}</div></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='meta'>{m['time']}</div>", unsafe_allow_html=True)

# --- Main Layout ---
col1, col2 = st.columns([3, 1])

with col1:
    st.header("🏙️ City Assistant — Санкт-Петербург")

    # --- Быстрые вопросы сразу под заголовком ---
    st.markdown("### 🚀 Быстрые вопросы")
    col_q1, col_q2, col_q3 = st.columns(3)

    with col_q1:
        if st.button("🏛️ Достопримечательности", use_container_width=True, key="btn_attractions"):
            st.session_state.messages.append(
                {"role": "user", "text": "Какие достопримечательности посмотреть в Санкт-Петербурге?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Какие достопримечательности посмотреть в Санкт-Петербурге?")
            # =============================================================================
            response = st.session_state.assistant.process_query("достопримечательности")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

        if st.button("📄 Госуслуги", use_container_width=True, key="btn_gosuslugi"):
            st.session_state.messages.append(
                {"role": "user", "text": "Какие госуслуги можно получить онлайн?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Какие госуслуги можно получить онлайн?")
            # =============================================================================
            response = st.session_state.assistant.process_query("госуслуги")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

    with col_q2:
        if st.button("🚇 Метро", use_container_width=True, key="btn_metro"):
            st.session_state.messages.append(
                {"role": "user", "text": "Как работает метро в Санкт-Петербурге?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Как работает метро в Санкт-Петербурге?")
            # =============================================================================
            response = st.session_state.assistant.process_query("метро")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

        if st.button("🏠 МФЦ", use_container_width=True, key="btn_mfc"):
            st.session_state.messages.append(
                {"role": "user", "text": "Где найти МФЦ и какие услуги они предоставляют?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Где найти МФЦ и какие услуги они предоставляют?")
            # =============================================================================
            response = st.session_state.assistant.process_query("мфц")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

    with col_q3:
        if st.button("👶 Детский сад", use_container_width=True, key="btn_kindergarten"):
            st.session_state.messages.append(
                {"role": "user", "text": "Как записать ребенка в детский сад?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Как записать ребенка в детский сад?")
            # =============================================================================
            response = st.session_state.assistant.process_query("детский сад")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

        if st.button("💸 Субсидии ЖКХ", use_container_width=True, key="btn_subsidies"):
            st.session_state.messages.append(
                {"role": "user", "text": "Как получить субсидию на ЖКХ?", "time": get_local_time()})
            # =============================================================================
            # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
            # =============================================================================
            # response = st.session_state.assistant.process_user_query("user_123", "Как получить субсидию на ЖКХ?")
            # =============================================================================
            response = st.session_state.assistant.process_query("субсидии жкх")
            st.session_state.messages.append(
                {"role": "assistant", "text": response, "time": get_local_time()})
            st.rerun()

    st.markdown("---")

    # Простой контейнер для сообщений
    messages_area = st.container()
    with messages_area:
        render_messages()

    # --- User input в самом низу основной колонки ---
    st.markdown("---")
    user_input = st.chat_input("Введите ваш вопрос о Санкт-Петербурге...")

# --- Sidebar ---
with col2:
    st.subheader("🔧 Статус системы")
    
    # Проверка доступности компонентов
    components_status = {
        "Интерфейс": "✅ Активен",
        "База знаний": "🔄 В разработке", 
        "Поиск": "🔄 В разработке",
        "AI Модель": "🔄 В разработке"
    }
    
    for component, status in components_status.items():
        st.write(f"{component}: {status}")
    
    st.markdown("---")
    st.subheader("⚙️ Управление")

    if st.button("🗑️ Очистить историю", use_container_width=True, key="btn_clear"):
        st.session_state.messages = _default_history()
        st.rerun()

    if st.button("💾 Экспорт чата", use_container_width=True, key="btn_export"):
        chat_data = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Скачать историю",
            data=chat_data,
            file_name=f"city_assistant_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

    st.markdown("---")
    st.subheader("ℹ️ Информация")
    st.info("""
**City Assistant** помогает с:

• Госуслугами и документами
• Достопримечательностями  
• Транспортом и маршрутами
• МФЦ и учреждениями
• Субсидиями и льготами

*Версия: 1.0 (Демо)*
""")

# Обработка обычного ввода пользователя
if user_input:
    # Сохраняем сообщение пользователя
    st.session_state.messages.append(
        {"role": "user", "text": user_input, "time": get_local_time()})

    # Показываем индикатор набора сообщения
    with st.spinner("City Assistant думает..."):
        time.sleep(1)  # Имитация обработки
        
        # =============================================================================
        # БУДУЩАЯ РЕАЛЬНАЯ ИНТЕГРАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
        # =============================================================================
        # # Реальная обработка через пайплайн
        # result = st.session_state.assistant.process_user_query("user_123", user_input)
        # assistant_reply = result['response']
        # =============================================================================
        
        # Временная обработка через mock
        assistant_reply = st.session_state.assistant.process_query(user_input)
    
    # Добавляем ответ ассистента
    st.session_state.messages.append(
        {"role": "assistant", "text": assistant_reply, "time": get_local_time()})

    st.rerun()

# =============================================================================
# БУДУЩАЯ РЕАЛЬНАЯ ИНИЦИАЛИЗАЦИЯ - РАСКОММЕНТИРОВАТЬ КОГДА КОМПОНЕНТЫ БУДУТ ГОТОВЫ
# =============================================================================
# # Инициализация полноценной системы при первом запуске
# if "pipeline_initialized" not in st.session_state:
#     with st.spinner("Инициализация City Assistant..."):
#         st.session_state.assistant.initialize_knowledge_base()
#         st.session_state.pipeline_initialized = True
# =============================================================================