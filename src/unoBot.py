import telebot
from telebot import types
import logic
from threading import Thread

bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')
threadsByChatId = {}

#начальное приветствие
@bot.message_handler(commands=['start'])
def main(info):
    bot.send_message(info.chat.id, 'Этот бот предназначен для проведения игры уно в телеграмме. Для запуска игры добавьте бота в свою группу, и напишите /start_game.')


#запуск создания игры
@bot.message_handler(commands=['start_game'])
def main(info):
    if logic.isGameRunning(info.chat.id):
        bot.send_message(info.chat.id, 'Не тупи, игра уже идёт.')
        return

    logic.games_byId[info.chat.id] = logic.game(info.chat.id)
    print(info.chat.id)
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
    for player in logic.games_byId[info.chat.id].players:
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
    if logic.games_byId[info.chat.id].isRunning:
        markup = telebot.types.ReplyKeyboardRemove()
        logic.games_byId[info.chat.id].isRunning = False
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

@bot.message_handler(commands=['help_game'])
def main(info):
    msg = 'Игра UNO предназначена для 2 до 10 игроков. Каждый игрок получает по 7 карт, а одна карта остается в центре как “ведущая” карта. Все карты имеют номера от 1 до 9 и два специальных значения: “Реверс” и “+2”. Цель игры - быть первым, кто избавится от всех своих карт. \n Правила игры: \n1. Игроки ходят по часовой стрелке. \n2. Каждый игрок должен положить карту соответствующего цвета или значения, если возможно(чёрные карты можно положить по верх любой из карт, после этого игрок выбирает цвет, который будет главным после этой карты). \n3. Если игрок не может положить подходящую карту, он берет одну карту из колоды ,и если после этого он до сих пор не может сходить, то пропускает ход. \n4. При выпадении “Реверса”, все игроки должны поменять направление своего хода. \n5. Карта “+2” заставляет следующего игрока взять две карты.\n 6. Победителем становится последний игрок, без карт.\n 7. Остальные места распределяются по количеству баллов(баллы считаются в зависимости от оставшихся карт в руке)'
    bot.send_message(info.chat.id, msg)

#Присоединение игрока после начала игры
@bot.message_handler(commands=['join'])
def message_reply(info):
    if info.from_user.username not in logic.games_byId[info.chat.id].player_hasActed:
        bot.send_message(info.chat.id, f'Игрок {info.from_user.username} добавлен')
        logic.games_byId[info.chat.id].add_player(info.from_user.username, info.from_user.id)


#запуск игры
@bot.message_handler(commands=['play'])
def message_reply(info):
    keyboard = telebot.types.ReplyKeyboardRemove()

    #проверка на условия запуска игры
    if logic.games_byId[info.chat.id].isRunning:
        bot.send_message(info.chat.id, "Что-то пошло не так(", reply_markup=keyboard)
        return

    bot.send_message(info.chat.id, "Да начнётся игра!!!))", reply_markup=keyboard)
    logic.games_byId[info.chat.id].isRunning = True
    
    threadsByChatId[info.chat.id] = Thread(target=logic.games_byId[info.chat.id].game)
    threadsByChatId[info.chat.id].start()

#очистка полей кнопок
@bot.message_handler(commands=['clear'])
def message_reply(info):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(info.chat.id, "Очищаю кнопочки", reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(info):
    if info.text=="Присоединиться":
        if info.from_user.username not in logic.games_byId[info.chat.id].player_hasActed:
            bot.send_message(info.chat.id, f'Игрок {info.from_user.username} добавлен')
            logic.games_byId[info.chat.id].add_player(info.from_user.username, info.from_user.id)

    if info.text=="Начать игру":
        markup = telebot.types.ReplyKeyboardRemove()
        if logic.games_byId[info.chat.id].isRunning or len(logic.games_byId[info.chat.id].players) == 0:
            bot.send_message(info.chat.id, "Что-то пошло не так(", reply_markup=markup)
            return
        bot.send_message(info.chat.id, "Да начнётся игра!!!))", reply_markup=markup)
        logic.games_byId[info.chat.id].isRunning = True
        threadsByChatId[info.chat.id] = Thread(target=logic.games_byId[info.chat.id].game)
        threadsByChatId[info.chat.id].start()

    if logic.games_byId[info.chat.id].isRunning:
        player = info.from_user.username
        if (info.text == "Взять карту" or info.text == "Пропуск хода") and logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player:
            logic.games_byId[info.chat.id].player_hasActed[player] = True
            logic.games_byId[info.chat.id].player_lastMove[player] = -1
        if logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player and any(info.text == logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards[ind].name for ind in range(len(logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards))):
            for ind in range(len(logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards)):
                if info.text == logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards[ind].name:
                    
                    logic.games_byId[info.chat.id].player_hasActed[player] = True
                    logic.games_byId[info.chat.id].player_lastMove[player] = int(ind)
                    break
    
    if logic.games_byId[info.chat.id].isRunning:
        player = info.from_user.username
        if logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player and logic.games_byId[info.chat.id].next_color is False and info.text in '🟩🟨🟦🟥':
            logic.games_byId[info.chat.id].player_hasActed[player] = True
            match info.text:
                case '🟩':
                    logic.games_byId[info.chat.id].next_color = 'green'
                case '🟨':
                    logic.games_byId[info.chat.id].next_color = 'yellow'
                case '🟦':
                    logic.games_byId[info.chat.id].next_color = 'blue'
                case '🟥':
                    logic.next_color = 'red'
