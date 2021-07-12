import telebot
from telebot import types
import requests
import json


import config
import mailag
import db


bot = telebot.TeleBot(config.token)
mailflag = 0
codeflag = 0
adminflag = 0
postadminflag = 0
invite = config.inv_link
bad_email = config.bad_mail


@bot.message_handler(commands=['help', 'start'])
def start_chat(message):
    global mailflag
    mailflag = 1
    bot.send_message(message.from_user.id, "Напишите ваш email отправки кода")


@bot.message_handler(commands=['admin'])
def admin(message):
    global adminflag
    global codeflag
    codeflag = 0
    adminflag = 1
    bot.send_message(message.from_user.id, "введите пароль")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global mailflag
    global codeflag
    global invite
    global bad_email
    global postadminflag
    global adminflag
    if mailflag == 1:
        answer = requests.post(config.url + 'code/send/', data=json.dumps({'name': str(message.chat.id), 'email': message.text}), headers=config.headers).json()
        print(answer)
        print(message.text, 'email')
        mailflag = 0
        codeflag = 1
        keyboard = types.InlineKeyboardMarkup()
        email_button = types.InlineKeyboardButton(text='Изменить email', callback_data='email')
        code_button = types.InlineKeyboardButton(text='Переслать код', callback_data='code')
        keyboard.add(email_button)
        keyboard.add(code_button)
        bot.send_message(message.from_user.id, "Введите код или выберете один из вариантов", reply_markup=keyboard)
    elif codeflag == 1:
        answer = requests.get(config.url + 'code/get/', data=json.dumps({'name': str(message.chat.id)}), headers=config.headers).json()
        print(answer)
        print(message.text, 'code')
        if answer['code'] == 'to many attempts':
            bot.send_message(message.from_user.id, "слишком много попыток ввода")
        elif answer['code'] == 'time is over':
            bot.send_message(message.from_user.id, "время действия кода истекло - запросите новый")
        elif answer['code'] == message.text:
            bot.send_message(message.from_user.id, invite)
            codeflag = 0
        else:
            bot.send_message(message.from_user.id, "вы ввели неверный код")
            mailag.send_message(bad_email, 'попытка авторизации на почту: ' + db.get_email(str(message.chat.id)))
    elif adminflag == 1:
        adminflag = 0
        if message.text == config.admin_pass:
            postadminflag = 1
            bot.send_message(message.from_user.id, "введите новую почту или новую ссылку приглашение")
        else:
            bot.send_message(message.from_user.id, "вы ввели неверный пароль")
    elif postadminflag == 1:
        if '@' in message.text:
            bad_email = message.text
        else:
            invite = message.text
    else:
        bot.send_message(message.from_user.id, "Напиши /help что бы начать")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global mailflag
    global codeflag
    try:
        if call.message:
            if call.data == "email":
                mailflag = 1
                codeflag = 0
                bot.send_message(call.message.chat.id, "Введите новый email")
            if call.data == "code":
                codeflag = 1
                mailflag = 0
                answer = requests.post(config.url + 'code/resend/', data=json.dumps({'name' :str(call.message.chat.id)}), headers=config.headers).json()
                print(answer)
                bot.send_message(call.message.chat.id, "Введите новый код")
    except Exception as e:
        print('err')


bot.polling(none_stop=True, interval=0)
