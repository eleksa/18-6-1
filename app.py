import telebot
from config import TOKEN, available_currencies
from extensions import APIException, Converter


my_bot = telebot.TeleBot(TOKEN)


# обработчик команд /start, /help
@my_bot.message_handler(commands=['start', 'help'])
def start_command(message: telebot.types.Message):
    text = 'Для конвертации валюты отправь команду в формате:\n' \
           '<название валюты которую покупаешь> <название валюты за которую покупаешь> <количество покупаемой ' \
           'валюты>\nДля получения списка доступных валют отправь команду /values.\n' \
           'Для получения справки по работе бота отправь команду /help. '
    my_bot.reply_to(message, text)


# обработчик команды /values (получить список доступных валют)
@my_bot.message_handler(commands=['values'])
def list_avialable_command(message: telebot.types.Message):
    text = 'Доступны валюты: '
    for item in available_currencies.keys():
        text = '\n'.join((text, item))
    my_bot.reply_to(message, text)


# обработчик конвертации валют по 3-м параметрам
@my_bot.message_handler(content_types=['text'])
def currency_conversion(message: telebot.types.Message):
    try:
        user_data_input = message.text.split(' ')
        if len(user_data_input) != 3:
            raise APIException('Необходимо ввести 3 параметра для конвертации, или команду')
        base, quote, amount = user_data_input
        unit_price = Converter.get_price(base, quote, amount)
        total_base = unit_price * int(amount)
    except APIException as user_error:
        my_bot.reply_to(message, f'Пользовательская ошибка: {user_error}')
    except Exception as system_error:
        my_bot.reply_to(message, f'Ошибка при обработке запроса: {system_error}')
    else:
        text = f'По текущему курсу:\n{amount} {base} = {round(total_base, 4)} {quote}'
        my_bot.send_message(message.chat.id, text)


my_bot.polling()
