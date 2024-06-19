import time
import telebot
from telebot import types  

# Вставьте сюда ваш токен
api = telebot.TeleBot("7298870576:AAH1QnrQQKPWX7kR5HumR3IxCuc06ngbt6k")


# Глобальный словарь для хранения состояний пользователей
user_states = {}

# Константы для состояний
ASK_FIRST_NUMBER, ASK_SECOND_NUMBER = range(2)

def start(chat_id):
    user_states[chat_id] = {'state': ASK_FIRST_NUMBER}
    api.send_message(chat_id, "Добрый вечер! Введите общую сумму за день(руб):")

def handle_message(chat_id, text):
    # Проверяем состояние пользователя
    state = user_states.get(chat_id)
    
    if state and state.get('state') == ASK_FIRST_NUMBER:
        if text.isdigit():
            user_states[chat_id] = {'state': ASK_SECOND_NUMBER, 'first_number': int(text)}
            api.send_message(chat_id, "Введите количество клиентов за день:")
        else:
            api.send_message(chat_id, "Пожалуйста, введите корректное число.")
    
    elif state and state.get('state') == ASK_SECOND_NUMBER:
        if text.isdigit():
            first_number = state['first_number']
            second_number = int(text)
            result = ((first_number / second_number) / 13 - 100)
            api.send_message(chat_id, f'Ваш средний чек: {result}%')
            del user_states[chat_id]
        else:
            api.send_message(chat_id, "Пожалуйста, введите корректное число.")
    
    else:
        api.send_message(chat_id, "Пожалуйста, начните с команды /start")

def handle_command(chat_id, text):
    if text == "/start":
        send_welcome(chat_id)

def send_welcome(chat_id):
    start_button = types.KeyboardButton(text = 'Начать')
    cancel_button = types.KeyboardButton(text = 'Отмена')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(start_button)
    keyboard.add(cancel_button)
    api.send_message(chat_id, "Добро пожаловать! Нажмите 'Начать', чтобы ввести числа, или 'Отмена' для завершения.", reply_markup=keyboard)

def main():
    offset = None
    while True:
        updates = api.get_updates(offset=offset, timeout=30)
        for update in updates:
            if hasattr(update, 'message'):
                chat_id = update.message.chat.id
                text = update.message.text

                if text == "Начать":
                    start(chat_id)
                elif text == "Отмена":
                    api.send_message(chat_id, "Операция отменена.")
                    if chat_id in user_states:
                        del user_states[chat_id]
                elif text.startswith("/"):
                    handle_command(chat_id, text)
                else:
                    handle_message(chat_id, text)
            
            offset = update.update_id + 1

        time.sleep(1)

if __name__ == '__main__':
    main()
