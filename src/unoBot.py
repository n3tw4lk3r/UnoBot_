import telebot
from telebot import types
import logic
bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')
CHAT_ID = None
#начальное приветствие
@bot.message_handler(commands=['start'])
def main(info):
    bot.send_message(info.chat.id, 'Этот бот предназначен для проведения игры уно в телеграмме. Для запуска игры добавьте бота в свою группу, и напишите /start_game.')


#запуск создания игры
@bot.message_handler(commands=['start_game'])
def main(info):
    if logic.game_is_running:
        bot.send_message(info.chat.id, 'Не тупи, игра уже идёт.')
        return

    logic.clear_fields()
    global CHAT_ID
    CHAT_ID = info.chat.id

    bot.send_message(info.chat.id,'''Охаё, они чан) Создай свою игру\n''')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Начать игру")
    button2 = types.KeyboardButton("Присоединиться")
    keyboard.add(button2, button1)

    bot.send_message(info.chat.id, 'Нажмите присоединиться, чтобы войти в игру. Нажмите начать игру, для запуска игры.', reply_markup=keyboard)


#Показывает игроков в игре
@bot.message_handler(commands=['stats'])
def main(info):
    msg = "Уважаемые игроки:\n"
    for player in logic.players:
        msg += str(player.name) + "\n"
    bot.send_message(info.chat.id, msg)


#Небольшая пасхалка
@bot.message_handler(commands=['stiker'])
def main(info):
    bot.send_sticker(info.chat.id, 'CAACAgIAAxkBAAEBpnZlPXSscqnvN_rM-uZusGxvanFG2wACuCQAArgGAUiH8Vp5cuhbHDAE')


#Принудительное завершение игры
@bot.message_handler(commands=['end_game'])
def main(info):
    #Проверяет была ли запущенна игра
    if logic.game_is_running:
        markup = telebot.types.ReplyKeyboardRemove()
        logic.game_is_running = False
    else:
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(info.chat.id, 'Игра не запущена(', reply_markup=markup)


#Вывод информации о создателях
@bot.message_handler(commands=['admin'])
def main(info):
    bot.send_message(info.chat.id, 'Писать по всем вопросам:@rbedin25, @shout_0_0, @n3tw4lk3r')



#Помощь с командами
@bot.message_handler(commands=['help'])
def main(info):
    msg = 'Сам себе помаги!\n Но если прям надо то: \n /start_game - запускает игру \n /end_game - заканчивает игру \n выбор картоы нажатием на кнопку в сообщениях\n /admin - связь с админами \n /join - присоедениться к игре \n /play- начать игру'
    bot.send_message(info.chat.id, msg)



#Присоединение игрока после начала игры
@bot.message_handler(commands=['join'])
def message_reply(info):
    if info.from_user.username not in logic.player_hasActed:
        bot.send_message(info.chat.id, f'Игрок {info.from_user.username} добавлен')
        logic.add_player(info.from_user.username, info.from_user.id)


#запуск игры
@bot.message_handler(commands=['play'])
def message_reply(info):
    keyboard = telebot.types.ReplyKeyboardRemove()

    #проверка на условия запуска игры
    if logic.game_is_running:
        bot.send_message(info.chat.id, "Что-то пошло не так(", reply_markup=keyboard)
        return

    global CHAT_ID
    bot.send_message(info.chat.id, "Да начнётся игра!!!))", reply_markup=keyboard)
    CHAT_ID = info.chat.id
    logic.game()

#очистка полей кнопок
@bot.message_handler(commands=['clear'])
def message_reply(info):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(info.chat.id, "Очищаю кнопочки", reply_markup=markup)



@bot.message_handler(content_types='text')
def message_reply(info):
    if info.text=="Присоединиться":
        if info.from_user.username not in logic.player_hasActed:
            bot.send_message(info.chat.id, f'Игрок {info.from_user.username} добавлен')
            logic.add_player(info.from_user.username, info.from_user.id)

    if info.text=="Начать игру":
        markup = telebot.types.ReplyKeyboardRemove()
        if logic.game_is_running or len(logic.players) == 0:
            bot.send_message(info.chat.id, "Что-то пошло не так(", reply_markup=markup)
            return
        global CHAT_ID
        bot.send_message(info.chat.id, "Да начнётся игра!!!))", reply_markup=markup)
        CHAT_ID = info.chat.id
        logic.game_is_running = True
        logic.game()


    if logic.game_is_running:
        player = info.from_user.username
        if (info.text == "Взять карту" or info.text == "Пропуск хода") and logic.players[logic.current_position].name == player:
            logic.player_hasActed[player] = True
            logic.player_lastMove[player] = -1
        if logic.players[logic.current_position].name == player and any(info.text == logic.players[logic.current_position].cards[ind].name for ind in range(len(logic.players[logic.current_position].cards))):
            for ind in range(len(logic.players[logic.current_position].cards)):
                if info.text == logic.players[logic.current_position].cards[ind].name:
                    logic.player_hasActed[player] = True
                    logic.player_lastMove[player] = int(ind)
                    break
    if logic.game_is_running:
        player = info.from_user.username
        if logic.players[logic.current_position].name == player and logic.next_color == False and info.text in '🟩🟨🟦🟥':
            logic.player_hasActed[player] = True
            match info.text:
                case '🟩':
                    logic.next_color = 'green'
                case '🟨':
                    logic.next_color = 'yellow'
                case '🟦':
                    logic.next_color = 'blue'
                case '🟥':
                    logic.next_color = 'red'
