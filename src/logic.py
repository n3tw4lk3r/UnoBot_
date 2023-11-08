import numpy as np
import unoBot
from telebot import types
import telebot
# -*- coding: UTF-8 -*-
class card:
    def __init__(self, num, col, step, count_cards, name_of_card, stiker_id):
        if num == 'universal':
            self.number = -1
        else:
            self.number = int(num)
        self.color = col
        if step[:step.find(' ')] == 'forward':
            self.change_of_step = int(step[step.find(' ') + 1:])
        elif step[:step.find(' ')] == 'back':
            self.change_of_step = - int(step[step.find(' ') + 1:])
        elif step[:step.find(' ')] == 'through':
            self.change_of_step = int(step[step.find(' ') + 1:]) + 1
        self.cards_to_next_player = int(count_cards[1:])
        self.name = name_of_card
        self.stiker = stiker_id

class players:
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
    global player, player_hasActed
    player.append(players(name, iid))
    player_hasActed[name] = False
    for j in range(7):
        player[len(player) - 1].cards.append(take_top_card())

def can_put_card(ind):
    global player, top_of_deck, current_position
    if ((player[current_position].cards[ind].number == top_of_deck.number or player[current_position].cards[ind].color == top_of_deck.color)) or (player[current_position].cards[ind].number == -1 and player[current_position].cards[ind].color == 'universal') or (top_of_deck.number == -1 and top_of_deck.color == 'universal'):
        return True
    return False

def put_card(ind):
    global player, deck_of_cards, current_position, top_of_deck, step
    top_of_deck = player[current_position].cards[ind]
    player[current_position].cards = player[current_position].cards[:ind] + player[current_position].cards[ind + 1:]
    for i in range(top_of_deck.cards_to_next_player):
        player[(len(player) + current_position + step) % len(player)].cards.append(take_top_card())
    if top_of_deck.change_of_step == 1 or top_of_deck.change_of_step == -1:
        step *= top_of_deck.change_of_step
        current_position = (len(player) + current_position + step) % len(player)
    else:
        current_position = (len(player) + current_position + step * top_of_deck.change_of_step) % len(player)
    #print(current_position, step)

def game():
    global player, deck_of_cards, current_position, top_of_deck, step, player_hasActed, the_game_is_running, player_lastMove
    the_game_is_running = True
    current_position = 0
    step = 1
    top_of_deck = take_top_card()

    while the_game_is_running:
        markup = telebot.types.ReplyKeyboardRemove()
        #unoBot.bot.send_message(unoBot.CHAT_ID, 'верхняя карта: ' + top_of_deck.name, reply_markup=markup)
        unoBot.bot.send_sticker(unoBot.CHAT_ID, top_of_deck.stiker, reply_markup=markup)
        buttons = [types.KeyboardButton("Взять карту")]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, selective=True)
        for i in range(len(player[current_position].cards)):
            msgg = player[current_position].cards[i].name
            buttons.append(types.KeyboardButton(msgg))
        keyboard.add(*buttons)
        unoBot.bot.send_message(unoBot.CHAT_ID, '@' + player[current_position].name +' выбери номер карты, которую кинешь или возьми из колоды', reply_markup=keyboard)

        count_move = 0
        while True:
            try:
                a = player_hasActed[player[current_position].name]
            except IndexError:
                return
            while the_game_is_running and player_hasActed[player[current_position].name] == False:
                pass
            if the_game_is_running:
                player_hasActed[player[current_position].name] = False
                num = player_lastMove[player[current_position].name]
                if num == -1:
                    if count_move == 0:
                        player[current_position].cards.append(take_top_card())
                        num = len(player[current_position].cards) - 1
                        count_move += 1
                        if all(can_put_card(i) == False for i in range(len(player[current_position].cards))):
                            buttons = [unoBot.types.KeyboardButton("Пропуск хода")]
                        else:
                            buttons = [unoBot.types.KeyboardButton("Взять карту")]
                        keyboard = unoBot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5,  selective=True)
                        for i in range(len(player[current_position].cards)):
                            msgg = player[current_position].cards[i].name
                            buttons.append(unoBot.types.KeyboardButton(msgg))
                        keyboard.add(*buttons)
                        unoBot.bot.send_message(unoBot.CHAT_ID, '@' + player[current_position].name +" карта добавлена", reply_markup=keyboard)
                    else:
                        if all(can_put_card(i) == False for i in range(len(player[current_position].cards))):
                            unoBot.bot.send_message(unoBot.CHAT_ID, 'Лошарик, пропускаешь ход')
                            current_position = (len(player) + current_position + step) % len(player)
                            break
                        else:
                            unoBot.bot.send_message(unoBot.CHAT_ID, 'хватит тырить карты из колоды')
                else:
                    if can_put_card(num):
                        put_card(num)
                        break
                    else:
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'Дурачок попробуй ещё')
        if any(len(player[i].cards) == 0 for i in range(len(player))):
            for i in range(len(player)):
                if len(player[i].cards) == 0:
                    unoBot.bot.send_message(unoBot.CHAT_ID, f'ПОЗДРАВЛЯЕМ С ПОБЕДОЙ {player[i].name}')
            the_game_is_running = False
    markup = telebot.types.ReplyKeyboardRemove()
    unoBot.bot.send_message(unoBot.CHAT_ID, 'Игра закончилась ну блииииин(((09((09(((', reply_markup=markup)
    clear_fields()

def clear_fields():
    global player, player_hasActed, player_lastMove, deck_of_cards, current_position, the_game_is_running
    player = []
    player_hasActed = {}
    player_lastMove = {}
    deck_of_cards = []
    current_position = 0
    the_game_is_running = False
    #unoBot.bot.send_message(unoBot.CHAT_ID, 'все поля очищены')

file = open("UNO cards.txt", 'r')
cards = []
while True:
    mas = file.readline().strip()
    if not mas:
        break
    mas = mas.split('_')
    st = mas[5]
    i = 6
    while i < len(mas):
        st += '_' + mas[i]
        i += 1
    p = mas[4].split()
    s = ''
    for j in range(len(p)):
        if p[j][0] == '!':
            s += chr(int(p[j][1:]))
        else:
            s += p[j]
    cards.append(card(mas[0], mas[1], mas[2], mas[3], s, st))
file.close()

index_in_cards = [i for i in range(len(cards))]
player = []
player_hasActed = {}
player_lastMove = {}
deck_of_cards = []
current_position = 0
the_game_is_running = False
