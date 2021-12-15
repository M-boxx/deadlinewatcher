# DeadlineWatcher
import telebot
from telebot import types 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
SITUATION = None
DATE_MONTH = 1
DATE_DAY = 2

bot = telebot.TeleBot('5012802026:AAGeqsv5Qi2TrWmRcAz9anKDudxAQiWeAow')

# функция, отвечающая за начало программы
def start(update, context):

    update.message.reply_text('40 Приветствую! Я - бот, следящий за вашими дедлайнами')
    
    get_deadline_date(update, context)

# функция, отвечающая за получения даты дедлайна
def get_deadline_date(update, context):
    global SITUATION
    SITUATION = DATE_MONTH
    update.message.reply_text('Позвольте узнать, к какому по счёту месяцу вы хотите закончить работу?')


# функция, отвечающая за команду помощи
def help(update, context):
    update.message.reply_text('help command received')

# функция, отвечающая за ошибку, возникшую во время получения данных
def error(update, context):
    update.message.reply_text('an error occured')

# function to handle normal text 
def text(update, context):
    text_received = update.message.text
    
    global SITUATION

    if SITUATION==DATE_MONTH:
        return received_deadline_month(update, context)
    if SITUATION==DATE_DAY:
        received_deadline_day(update, context)

def received_deadline_month(update, context):
    global SITUATION

    try:
        text_received = update.message.text
        month = int(text_received)

        if month>12 or month<1:
            raise ValueError('Такого месяца не может быть')
        context.user_data['deadline_month'] = month
        update.message.reply_text('Прекрасно, теперь введите число этого месяца')
        SITUATION = DATE_DAY
    except:
        update.message.reply_text('Неправильный формат ввода')

def received_deadline_day(update, context):
    global SITUATION

    try:
        text_received = update.message.text
        day = int(text_received)

        if day>31 or day<1:
            raise ValueError('Такого дня быть не может')
        context.user_data['deadline_day'] = day
        update.message.reply_text('Дедлайн установлен')
        SITUATION = None
    except:
        update.message.reply_text('Неправильный формат ввода')

def deadline(update, context):
    now = datetime.datetime.now()
    update.message.reply_text(now.day)
    update.message.reply_text(now.month)

def main():
    TOKEN = "5012802026:AAGeqsv5Qi2TrWmRcAz9anKDudxAQiWeAow"

    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("deadline", deadline))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()