import telebot
from telebot import types
import webbrowser
import logic
bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')
CHAT_ID = None

@bot.message_handler(commands=['xxl'])
def main(info):
    webbrowser.open('https://rt.pornhub.com')

@bot.message_handler(commands=['xxx'])
def main(info):
    types.InlineKeyboardMarkup

@bot.message_handler(commands=['start'])
def main(info):
    bot.send_message(info.chat.id, 'Hello, first timers.')

@bot.message_handler(commands=['start_game'])
def main(info):
    global CHAT_ID
    CHAT_ID = info.chat.id
    bot.send_message(info.chat.id, 
    '''Охаё, они чан) Создай свою игру\n
    /add <Имя игрока> - добавление нового игрока\n
    /play             - начать игру\n
    /stats            - состояние игры
    '''
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Присоединиться")
    markup.add(item2, item1)
    bot.send_message(info.chat.id, 'Нажмите присоединиться, чтобы войти в игру. Нажмите начать игру, для запуска игры.', reply_markup=markup)

@bot.message_handler(commands=['stats'])
def main(info):
    msg = "Увожаемые игроки:\n"
    for p in logic.player:
        msg += str(p.name) + "\n"
    #bot.send_message(info.chat.id, msg)

@bot.message_handler(commands=['move'])
def main(info):
    move = info.text.split()[1]
    player = info.from_user.first_name
    if move.isdigit() and logic.player[logic.pos].name == player:
        logic.player_hasActed[player] = True
        logic.player_lastMove[player] = int(move)

@bot.message_handler(commands=['admin'])
def main(info):
    bot.send_message(info.chat.id, 'Писать по всем вопросам:@rbedin25, @shout_0_0, @n3tw4lk3r')

@bot.message_handler(commands=['help'])
def main(info):
    bot.send_message(info.chat.id, f'Сам себе помаги, {info.from_user.first_name}')

@bot.message_handler(commands=['button'])
def button_message(info):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(info.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Кнопка":
        bot.send_message(message.chat.id,"https://rt.pornhub.com")
    if message.text=="Присоединиться":
        bot.send_message(message.chat.id, f'Игрок {message.from_user.first_name} добавлен')
        logic.player.append(logic.players(message.from_user.first_name))
        logic.player_hasActed[message.from_user.first_name] = False
    if message.text=="Начать игру":
        global CHAT_ID
        CHAT_ID = message.chat.id
        bot.send_message(message.chat.id, 'Да начнётся игра!!111')
        logic.construct_game()
        bot.send_message(message.chat.id, 'Игра началась)))')
        logic.game()
        bot.send_message(message.chat.id, 'Игра закончилась ну блииииин(((09((09(((')
