import numpy as np
import unoBot
from telebot import types
import telebot
class card:
    def __init__(self, num, col, step, count_cards, name_of_card, stiker_id):
        self.number = num
        self.color = col
        match step[:step.find(' ')]:
            case 'forward':
                self.change_of_step = int(step[step.find(' ') + 1:])
            case 'back':
                self.change_of_step = - int(step[step.find(' ') + 1:])
            case 'through':
                self.change_of_step = int(step[step.find(' ') + 1:]) + 1
        self.cards_to_next_player = int(count_cards[1:])
        self.name = name_of_card
        self.stiker = stiker_id

class player:
    def __init__(self, st, idd):
        self.name = st
        self.cards = []
        self.id = idd


def new_deck():
    global deck_of_cards, index_in_cards, cards
    index_in_cards = np.random.permutation(index_in_cards)
    deck_of_cards = []
    for i in range(len(index_in_cards)):
        deck_of_cards.append(cards[index_in_cards[i]])


def take_top_card():
    global deck_of_cards
    if len(deck_of_cards) == 0:
        new_deck()
    ans = deck_of_cards[0]
    deck_of_cards = deck_of_cards[1:]
    return ans

def add_player(name, iid):
    global players, player_hasActed
    players.append(player(name, iid))
    player_hasActed[name] = False
    for j in range(7):
        players[len(players) - 1].cards.append(take_top_card())

def can_put_card(ind):
    global players, top_of_deck, current_position
    if ((players[current_position].cards[ind].number == top_of_deck.number or players[current_position].cards[ind].color == top_of_deck.color)) or (players[current_position].cards[ind].number == 'universal' and players[current_position].cards[ind].color == 'universal'):
        return True
    return False

def put_card(ind):
    global players, deck_of_cards, current_position, top_of_deck, step, next_color, player_hasActed, game_is_running
    top_of_deck = players[current_position].cards[ind]
    players[current_position].cards = players[current_position].cards[:ind] + players[current_position].cards[ind + 1:]
    for i in range(top_of_deck.cards_to_next_player):
        players[(len(players) + current_position + step) % len(players)].cards.append(take_top_card())

    if top_of_deck.number == 'universal' and top_of_deck.color == 'universal':
        buttons = [types.KeyboardButton("🟦"), types.KeyboardButton("🟨"), types.KeyboardButton("🟥"), types.KeyboardButton("🟩")]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=True)
        keyboard.add(*buttons)
        unoBot.bot.send_message(unoBot.CHAT_ID, '@' + players[current_position].name + ' выбери будущий цвет', reply_markup=keyboard)
        next_color = False
        player_hasActed[players[current_position].name] = False
        while game_is_running and player_hasActed[players[current_position].name] == False:
            pass
        player_hasActed[players[current_position].name] = False
        top_of_deck.color = next_color

    if top_of_deck.change_of_step == 1 or top_of_deck.change_of_step == -1:
        step *= top_of_deck.change_of_step
        current_position = (len(players) + current_position + step) % len(players)
    else:
        current_position = (len(players) + current_position + step * top_of_deck.change_of_step) % len(players)


def game():
    global players, deck_of_cards, current_position, top_of_deck, step, player_hasActed, game_is_running, player_lastMove
    game_is_running = True
    current_position = 0
    step = 1
    top_of_deck = take_top_card()

    while game_is_running:
        markup = telebot.types.ReplyKeyboardRemove()
        unoBot.bot.send_message(unoBot.CHAT_ID, 'Верхняя карта: ', reply_markup=markup)
        unoBot.bot.send_sticker(unoBot.CHAT_ID, top_of_deck.stiker)
        buttons = [types.KeyboardButton("Взять карту")]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=True)
        for i in range(len(players[current_position].cards)):
            msg = players[current_position].cards[i].name
            buttons.append(types.KeyboardButton(msg))
        keyboard.add(*buttons)
        unoBot.bot.send_message(unoBot.CHAT_ID, '@' + players[current_position].name +' выбери номер карты, которую кинешь или возьми из колоды', reply_markup=keyboard)

        card_was_taken = False
        while True:
            while game_is_running and player_hasActed[players[current_position].name] == False:
                pass
            player_hasActed[players[current_position].name] = False
            if not game_is_running:
                break
            num_in_players_cards = player_lastMove[players[current_position].name]
            if num_in_players_cards == -1:
                if card_was_taken == False:
                    card_was_taken = True
                    players[current_position].cards.append(take_top_card())
                    num_in_players_cards = len(players[current_position].cards) - 1
                    if all(can_put_card(i) == False for i in range(len(players[current_position].cards))):
                        buttons = [unoBot.types.KeyboardButton("Пропуск хода")]
                    else:
                        buttons = [unoBot.types.KeyboardButton("Взять карту")]
                    keyboard = unoBot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4,  selective=True)
                    for i in range(len(players[current_position].cards)):
                        msgg = players[current_position].cards[i].name
                        buttons.append(unoBot.types.KeyboardButton(msgg))
                    keyboard.add(*buttons)
                    unoBot.bot.send_message(unoBot.CHAT_ID, '@' + players[current_position].name +" карта добавлена", reply_markup=keyboard)
                else:
                    if all(can_put_card(i) == False for i in range(len(players[current_position].cards))):
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'Лошарик, пропускаешь ход')
                        current_position = (len(players) + current_position + step) % len(players)
                        break
                    else:
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'хватит тырить карты из колоды')
            else:
                if can_put_card(num_in_players_cards):
                    put_card(num_in_players_cards)
                    break
                else:
                    unoBot.bot.send_message(unoBot.CHAT_ID, 'Дурачок попробуй ещё')
        if any(len(players[i].cards) == 0 for i in range(len(players))):
            for i in range(len(players)):
                if len(players[i].cards) == 0:
                    unoBot.bot.send_message(unoBot.CHAT_ID, f'ПОЗДРАВЛЯЕМ С ПОБЕДОЙ @{players[i].name}')
            game_is_running = False
    markup = telebot.types.ReplyKeyboardRemove()
    unoBot.bot.send_message(unoBot.CHAT_ID, 'Игра закончилась ну блииииин(((09((09(((', reply_markup=markup)
    clear_fields()

def clear_fields():
    global players, player_hasActed, player_lastMove, deck_of_cards, current_position, game_is_running, next_color
    players = []
    player_hasActed = {}
    player_lastMove = {}
    deck_of_cards = []
    current_position = 0
    game_is_running = False
    next_color = False

file = open("UNO cards.txt", 'r')
cards = []
while True:
    mas = file.readline().strip()
    if not mas:
        break
    mas = mas.split('~')
    p = mas[4].split()
    s = ''
    for j in range(len(p)):
        if p[j][0] == '!':
            s += chr(int(p[j][1:])) + ' '
        else:
            s += p[j] + ' '
    s = s[:-1]
    cards.append(card(mas[0], mas[1], mas[2], mas[3], s, mas[5]))
file.close()

index_in_cards = [i for i in range(len(cards))]
clear_fields()
