# DeadlineWatcher
import telebot
from telebot import types 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
SITUATION = None
DATE_MONTH = 1
DATE_DAY = 2

bot = telebot.TeleBot('5012802026:AAGeqsv5Qi2TrWmRcAz9anKDudxAQiWeAow')

deadline_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttonget = types.KeyboardButton('Установить дедлайн')
    buttonshow = types.KeyboardButton('Посмотреть дедлайн')
    markup.add(buttonget)
    markup.add(buttonshow)
    bot.send_message(message.chat.id, '51 Приветствую! Я - бот, следящий за вашими дедлайнами\nЕсли вы хотите установить новый дедлайн используйте кнопку "Установить дедлайн", для просмотра дедлайна используй "Посмотреть дедлайн"', reply_markup=markup)

    

# функция, отвечающая за получения даты дедлайна
def get_deadline_date(message):
    global SITUATION
    SITUATION = DATE_MONTH
    bot.send_message(message.chat.id, 'Позвольте узнать, к какому по счёту месяцу вы хотите закончить работу?')


# функция, отвечающая за команду помощи
def help(message):
    bot.send_message(message.chat.id, 'help command received')

# функция, отвечающая за ошибку, возникшую во время получения данных
def error(message):
    bot.send_message(message.chat.id, 'об Астралис')

@bot.message_handler(content_types=["text"])
def text(message):
    text_received = message.text
    
    if text_received=='Установить дедлайн':
        return get_deadline_date(message)
    if text_received=='Посмотреть дедлайн':
        return deadline_check(message)


    global SITUATION
    if SITUATION==DATE_MONTH:
        return received_deadline_month(message)
    if SITUATION==DATE_DAY:
        return received_deadline_day(message)

def received_deadline_month(message):
    global SITUATION

    try:
        text_received = message.text
        month = int(text_received)

        if month>12 or month<1:
            raise ValueError('Такого месяца не может быть')
        deadline_data[f'{message.chat.id}deadline_month'] = month
        bot.send_message(message.chat.id, 'Прекрасно, теперь введите число этого месяца')
        SITUATION = DATE_DAY
    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода')

def received_deadline_day(message):
    global SITUATION

    try:
        text_received = message.text
        day = int(text_received)

        if day>31 or day<1:
            raise ValueError('Такого дня быть не может')
        deadline_data[f'{message.chat.id}deadline_day'] = day
        bot.send_message(message.chat.id, 'Дедлайн установлен')
        SITUATION = None
    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода')

def deadline_check(message):
    now = datetime.datetime.now()
    userid = message.chat.id
    #bot.send_message(message.chat.id, now.day)
    #bot.send_message(message.chat.id, now.month)
    try:
        saved_day = deadline_data[f'{userid}deadline_day']
        saved_month = deadline_data[f'{userid}deadline_month']
        bot.send_message(userid, f'Дедлайн назначен на {saved_day}.{saved_month}!')
    except:
        bot.send_message(userid, 'Дедлайн не был установлен ранее')

if __name__ == '__main__':
    bot.infinity_polling()