# DeadlineWatcher
import telebot
from telebot import types 
import datetime
import config

DATE_MONTH = 1
DATE_DAY = 2
CHOOSE_LENGTH = 3
DEADLINE_TASKS = 11
DEADLINE_WORDS = 12
DEADLINE_PAGES = 13
SEND_WORK = 21
SEND_TASK = 22

bot = telebot.TeleBot(config.TOKEN)

deadline_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):

    """Эта функция является стартовой для пользователя и создаёт интерфейс"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttonget = types.KeyboardButton('Установить дедлайн')
    buttonshow = types.KeyboardButton('Посмотреть дедлайн')
    buttonsend = types.KeyboardButton('Отправить работу')
    markup.add(buttonget)
    markup.add(buttonshow)
    markup.add(buttonsend)
    bot.send_message(message.chat.id, 'Приветствую! Я - DeadlineWatcher 80 версии, следящий за вашими дедлайнами\nЕсли вы хотите установить новый дедлайн используйте кнопку "Установить дедлайн", для просмотра дедлайна кнопка "Посмотреть дедлайн", после установки дедлайна используйте кнопку "Отправить работу" для изменения прогресса выполнения задач', reply_markup=markup)

def get_deadline_date(message):
    
    """Данная функция запрашивает у пользователя месяц дедлайна, изменяя состояние бота на получение месяца"""

    deadline_data[message.chat.id] = DATE_MONTH
    bot.send_message(message.chat.id, 'Позвольте узнать, к какому месяцу вы хотите закончить работу?\nВведите цифру от 1 до 12')

@bot.message_handler(commands=['help'])
def help(message):

    """Функция help нужна для пояснения функций кнопок"""

    bot.send_message(message.chat.id, 'Используйте команду "Установить дедлайн", если вы хотите изменить размер дедлайна или его дату')
    bot.send_message(message.chat.id, 'Используйте команду "Посмотреть дедлайн", если вы установили дедлайн и хотите узнать прогресс завершения работы')
    bot.send_message(message.chat.id, 'А для изменения прогресса работы используйте "Отправить работу"')
    
def error(message):

    """Функция для непредвиденных ошибок"""

    bot.send_message(message.chat.id, 'Произошла непредвиденная ошибка')

@bot.message_handler(content_types=["text"])
def text(message):

    """Данная функция обрабатывает состояние программы и включает соответствующую функцию, в зависимости от полученной информации"""

    text_received = message.text
    
    if text_received=='Установить дедлайн':
        return get_deadline_date(message)
    if text_received=='Посмотреть дедлайн':
        return deadline_check(message)
    if text_received=='Отправить работу':
        return work_check(message)

    
    if deadline_data[message.chat.id]==DATE_MONTH:
        return received_deadline_month(message)
    if deadline_data[message.chat.id]==DATE_DAY:
        return received_deadline_day(message)
    if deadline_data[message.chat.id]==CHOOSE_LENGTH:
        return received_deadline_length(message)
    if deadline_data[message.chat.id]==SEND_WORK or deadline_data[message.chat.id]==SEND_TASK:
        return received_deadline_work(message)

def work_check(message):

    """Данная функция запрашивает выполненную работу"""

    if deadline_data[f'{message.chat.id}deadline_len']!=0:
        if deadline_data[f'{message.chat.id}deadline_type']==DEADLINE_TASKS:
            deadline_data[message.chat.id] = SEND_TASK
            bot.send_message(message.chat.id, 'Напишите сколько заданий вы выполнили')

        else:
            deadline_data[message.chat.id] = SEND_WORK
            bot.send_message(message.chat.id, 'Отправьте вашу работу, я посчитаю её длину за вас')
    else:
        bot.send_message(message.chat.id, 'Ваш дедлайн не был установлен ранее')

def received_deadline_work(message):
    
    """Данная функция обрабатывает полученную работу и изменяет количество оставшейся работы"""

    try:
        text_received = message.text
        tasks = 0
        if(deadline_data[message.chat.id]==SEND_TASK):
            tasks = int(text_received)
        elif (deadline_data[message.chat.id]==SEND_WORK):
            written = str(text_received)
            tasks = count_words(written)

        if deadline_data[f'{message.chat.id}deadline_type']==DEADLINE_PAGES:
            tasks/=400

        if tasks<=0:
            raise ValueError('Маловато заданий')
        deadline_data[f'{message.chat.id}deadline_len'] -= tasks
        if deadline_data[f'{message.chat.id}deadline_len']<0:
            bot.send_message(message.chat.id, 'Прекрасная работа! Вы смогли перевыполнить задание!')
            deadline_data[f'{message.chat.id}deadline_len'] = 0
        elif deadline_data[f'{message.chat.id}deadline_len']==0:
            bot.send_message(message.chat.id, 'Поздравляю! Вы выполнили задание')
        else:
            percent = deadline_data[f'{message.chat.id}deadline_len']/deadline_data[f'{message.chat.id}deadline_maxlen']
            percent*=100
            bot.send_message(message.chat.id, f'Хорошая работа! Вам осталось сделать {percent:.2f}%')
        deadline_data[message.chat.id] = None

    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода работы (Задания измеряются в числах, а текст я посчитаю сам)')

def count_words(string):

    """Данная функция считает слова в курсовой работе студента"""

    isinword = 0
    words = 0
    for letter in string:
        if letter!=' ' and letter!='\n' and isinword==0:
            words+=1
            isinword = 1
        elif letter==' ' or letter=='\n':
            isinword = 0
    return words

def received_deadline_month(message):
    
    """Данная функция получает месяц дедлайна и обрабатывает значение"""

    try:
        text_received = message.text
        month = int(text_received)

        if month>12 or month<1:
            raise ValueError('Такого месяца не может быть')
        deadline_data[f'{message.chat.id}deadline_month'] = month
        bot.send_message(message.chat.id, 'Прекрасно, теперь введите число этого месяца')
        deadline_data[message.chat.id] = DATE_DAY
    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода месяца')

def received_deadline_day(message):

    """Данная функция получает день дедлайна и обрабатывает значение"""

    try:
        text_received = message.text
        day = int(text_received)

        if day>31 or day<1:
            raise ValueError('Такого дня быть не может')
        deadline_data[f'{message.chat.id}deadline_day'] = day

        received_deadline_type(message)
    
    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода дня')

def received_deadline_type(message):

    """Конструкция реализации кнопок и обработки данных взята с pocketadmin.tech, статья о Telebot"""
    deadline_data[message.chat.id] = None
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Задания', callback_data=DEADLINE_TASKS))
    markup.add(telebot.types.InlineKeyboardButton(text='Слова', callback_data=DEADLINE_WORDS))
    markup.add(telebot.types.InlineKeyboardButton(text='Страницы', callback_data=DEADLINE_PAGES))
    bot.send_message(message.chat.id, text="Хорошо, а в чём вы будете измерять прогресс своей работы?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):    

    """Слушатель нажатий кнопок функции received_deadline_type()"""

    answer = ''
    if call.data == '11':
        answer = 'Ваш прогресс будет измеряться в заданиях!'
        deadline_data[f'{call.message.chat.id}deadline_type'] = DEADLINE_TASKS
    elif call.data == '12':
        answer = 'Ваш прогресс будет измеряться в словах!'
        deadline_data[f'{call.message.chat.id}deadline_type'] = DEADLINE_WORDS
    elif call.data == '13':
        answer = 'Ваш прогресс будет измеряться в страницах!'
        deadline_data[f'{call.message.chat.id}deadline_type'] = DEADLINE_PAGES

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Какой длины должна быть ваша работа?')
    if call.data=='13': bot.send_message(call.message.chat.id, 'Учитывайте, что вместимость страницы на 14 кегль Times New Roman примерно равна 400 словам')
    deadline_data[call.message.chat.id] = CHOOSE_LENGTH

def received_deadline_length(message):
    
    """Данная функция получает длину дедлайна и устанавливает в словарь"""

    try:
        text_received = message.text
        deadline_len = int(text_received)
        if deadline_len<1:
            raise ValueError('Слишком маленькая работа, тут мои полномочия всё')
        deadline_data[f'{message.chat.id}deadline_len'] = deadline_len
        deadline_data[f'{message.chat.id}deadline_maxlen'] = deadline_len
        bot.send_message(message.chat.id, 'Дедлайн установлен!')
        deadline_data[message.chat.id] = None

    except:
        bot.send_message(message.chat.id, 'Неправильный формат ввода длины')

def deadline_check(message):

    """Данная функция реализует кнопку Проверить дедлайн"""

    now = datetime.datetime.now()
    userid = message.chat.id
    try:
        saved_day = deadline_data[f'{userid}deadline_day']
        saved_month = deadline_data[f'{userid}deadline_month']
        bot.send_message(userid, f'Дедлайн назначен на {saved_day:02}.{saved_month:02}!')
        type = ''
        if deadline_data[f'{userid}deadline_type']==DEADLINE_TASKS: type = 'заданий'
        elif deadline_data[f'{userid}deadline_type']==DEADLINE_WORDS: type = 'слов'
        elif deadline_data[f'{userid}deadline_type']==DEADLINE_PAGES: type = 'страниц'
        lenvalue = deadline_data[f'{userid}deadline_len']

        if lenvalue<=0: bot.send_message(userid, f'Благодарю за своевременно выполненную работу, ваш DeadlineWatcher ♥')
        else: bot.send_message(userid, f'Вам осталось написать {lenvalue:.0f} {type}')
    except:
        bot.send_message(userid, 'Дедлайн не был полностью установлен ранее')

if __name__ == '__main__':
    bot.infinity_polling()