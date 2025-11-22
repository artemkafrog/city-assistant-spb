import streamlit as st
import time
from datetime import datetime
import pytz

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
        {"role": "assistant", "text": "Привет! Я City Assistant. Чем могу помочь?",
            "time": get_local_time()},
    ]


# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = _default_history()

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


# layout
col1, col2 = st.columns([3, 1])

with col1:
    st.header("City Assistant — Чат")

    # --- Быстрые вопросы сразу под заголовком ---
    st.markdown("### 🚀 Быстрые вопросы")
    col_q1, col_q2, col_q3 = st.columns(3)

    with col_q1:
        if st.button("🏛️ Достопримечательности", use_container_width=True, key="btn_attractions"):
            st.session_state.messages.append(
                {"role": "user", "text": "Какие достопримечательности посмотреть?", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "В Санкт-Петербурге рекомендую посетить: Эрмитаж, Петропавловскую крепость, Исаакиевский собор, Дворцовую площадь и Русский музей.", "time": get_local_time()})
            st.rerun()

        if st.button("🍽️ Где поесть", use_container_width=True, key="btn_food"):
            st.session_state.messages.append(
                {"role": "user", "text": "Где можно недорого поесть?", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "Рекомендую столовые 'Столовая №1', кафе 'Пышка' на Невском, фудкорты в торговых центрах. Средний чек: 300-500 рублей.", "time": get_local_time()})
            st.rerun()

    with col_q2:
        if st.button("🚇 Метро", use_container_width=True, key="btn_metro"):
            st.session_state.messages.append(
                {"role": "user", "text": "Как работает метро?", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "Метро работает с 5:30 до 00:30. Стоимость проезда 70 рублей. Есть безлимитные проездные на 1-30 дней.", "time": get_local_time()})
            st.rerun()

        if st.button("🏨 Отели", use_container_width=True, key="btn_hotels"):
            st.session_state.messages.append(
                {"role": "user", "text": "Посоветуйте недорогие отели", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "Бюджетные варианты: Ibis, Holiday Inn, отели на Васильевском острове. Цены от 2000 руб/ночь.", "time": get_local_time()})
            st.rerun()

    with col_q3:
        if st.button("🛍️ Шоппинг", use_container_width=True, key="btn_shopping"):
            st.session_state.messages.append(
                {"role": "user", "text": "Где лучше шоппинг?", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "Основные торговые центры: Гостиный двор, Апраксин двор, Галерея, Планета Нептун.", "time": get_local_time()})
            st.rerun()

        if st.button("🚕 Такси", use_container_width=True, key="btn_taxi"):
            st.session_state.messages.append(
                {"role": "user", "text": "Как вызвать такси?", "time": get_local_time()})
            st.session_state.messages.append(
                {"role": "assistant", "text": "Популярные такси: Яндекс Go, Ситимобил, Uber. Средняя цена поездки по центру 200-400 руб.", "time": get_local_time()})
            st.rerun()

    st.markdown("---")

    # Простой контейнер для сообщений
    messages_area = st.container()
    with messages_area:
        render_messages()

    # --- User input в самом низу основной колонки ---
    st.markdown("---")
    user_input = st.chat_input("Введите сообщение...")

# --- Sidebar ---
with col2:
    st.subheader("Статус")
    st.success("✅ Система активна")

    st.markdown("---")
    st.subheader("Управление")

    # Управление с подписями
    if st.button("🗑️ Очистить историю", use_container_width=True, key="btn_clear"):
        st.session_state.messages = _default_history()
        st.rerun()

    if st.button("📥 Экспорт чата", use_container_width=True, key="btn_export"):
        st.success("Чат экспортирован!")

    if st.button("🔍 Поиск по истории", use_container_width=True, key="btn_search"):
        st.info("Функция поиска")

    if st.button("🎨 Сменить тему", use_container_width=True, key="btn_theme"):
        st.info("Функция в разработке")

    st.markdown("---")
    st.subheader("Быстрые действия")

    # Быстрые действия с подписями
    if st.button("📍 Построить маршрут", use_container_width=True, key="btn_route"):
        st.session_state.messages.append(
            {"role": "user", "text": "Построй маршрут от вокзала до Эрмитажа", "time": get_local_time()})
        st.session_state.messages.append(
            {"role": "assistant", "text": "Маршрут от Московского вокзала до Эрмитажа: пешком по Невскому проспекту 25 минут, или на метро до станции Адмиралтейская.", "time": get_local_time()})
        st.rerun()

    if st.button("🕒 Ближайшие события", use_container_width=True, key="btn_events"):
        st.session_state.messages.append(
            {"role": "user", "text": "Какие события сегодня?", "time": get_local_time()})
        st.session_state.messages.append(
            {"role": "assistant", "text": "Сегодня: выставка в Русском музее, концерт в Мариинском театре, фестиваль на Дворцовой площади.", "time": get_local_time()})
        st.rerun()

    if st.button("🚨 Экстренная помощь", use_container_width=True, key="btn_emergency", type="secondary"):
        st.session_state.messages.append(
            {"role": "user", "text": "Нужна экстренная помощь", "time": get_local_time()})
        st.session_state.messages.append(
            {"role": "assistant", "text": "Экстренные службы: 112 - единый номер, 101 - пожарные, 102 - полиция, 103 - скорая. Говорите спокойно и четко.", "time": get_local_time()})
        st.rerun()

    st.markdown("---")
    st.subheader("Дополнительно")

    # Дополнительные функции с подписями
    if st.button("🔊 Озвучить сообщения", use_container_width=True, key="btn_voice"):
        st.info("Озвучивание сообщений")

    if st.button("⭐ Добавить в избранное", use_container_width=True, key="btn_favorite"):
        st.success("Добавлено в избранное!")

    if st.button("📱 Поделиться чатом", use_container_width=True, key="btn_share"):
        st.info("Функция поделиться")

    st.markdown("---")
    st.subheader("Информация")
    st.info("""
City Assistant помогает:

• Найти места в городе

• Построить маршруты

• Ответить на вопросы
""")

# Обработка обычного ввода пользователя
if user_input:
    # Сохраняем сообщение пользователя
    st.session_state.messages.append(
        {"role": "user", "text": user_input, "time": get_local_time()})

    # Генерируем ответ ассистента
    assistant_reply = f"Я получила ваше сообщение: '{user_input}'. Могу помочь с информацией по городу, маршрутам и достопримечательностям."

    # Добавляем ответ ассистента
    st.session_state.messages.append(
        {"role": "assistant", "text": assistant_reply, "time": get_local_time()})

    st.rerun()
