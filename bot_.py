import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')

# @bot.message_handler(commands=['xxl'])
# def main(info):
#     webbrowser.open('https://rt.pornhub.com')

@bot.message_handler(commands=['start'])
def main(info):
    bot.send_message(info.chat.id, 'Охаё, они чан)')

@bot.message_handler(commands=['admin'])
def main(info):
    bot.send_message(info.chat.id, 'Писать по всем вопросам:@rbedin25, @shout_0_0, @n3tw4lk3r')

@bot.message_handler(commands=['help'])
def main(info):
    bot.send_message(info.chat.id, f'Сам себе помаги, {info.from_user.first_name}')

@bot.message_handler(commands=['start_game'])
def main(info):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Присоединиться")
    markup.add(item2, item1)
    bot.send_message(info.chat.id, 'Нажмите присоединиться, чтобы войти в игру. Нажмите начать игру, для запуска игры.', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(info):
    if info.text=="Присоединиться":
        bot.send_message(info.chat.id, f'Игрок {info.from_user.first_name} добавлен')


bot.polling(none_stop=True)