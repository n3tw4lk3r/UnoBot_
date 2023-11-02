import numpy as np
import unoBot
from telebot import types

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
    global player, top_of_deck, pos
    if ((player[pos].cards[ind].number == top_of_deck.number or player[pos].cards[ind].color == top_of_deck.color)) or (player[pos].cards[ind].number == -1 and player[pos].cards[ind].color == 'universal') or (top_of_deck.number == -1 and top_of_deck.color == 'universal'):
        return True
    return False


def put_card(ind):
    global player, deck_of_cards, pos, top_of_deck, step
    top_of_deck = player[pos].cards[ind]
    player[pos].cards = player[pos].cards[:ind] + player[pos].cards[ind + 1:]
    for i in range(top_of_deck.cards_to_next_player):
        player[(len(player) + pos + step) % len(player)].cards.append(take_top_card())
    if top_of_deck.change_of_step == 1 or top_of_deck.change_of_step == -1:
        step *= top_of_deck.change_of_step
        pos = (len(player) + pos + step) % len(player)
    else:
        pos = (len(player) + pos + step * top_of_deck.change_of_step) % len(player)
    #print(pos, step)

def game():
    global player, deck_of_cards, pos, top_of_deck, step, player_hasActed, is_playing, player_lastMove
    is_playing = True
    pos = 0
    step = 1
    top_of_deck = take_top_card()
    while is_playing:
        unoBot.bot.send_message(unoBot.CHAT_ID, 'верхняя карта: ' + str(top_of_deck.name))
        unoBot.bot.send_sticker(unoBot.CHAT_ID, top_of_deck.stiker)
        msg = ""
        buttons = [types.KeyboardButton("/move")]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
        for i in range(len(player[pos].cards)):
            msg += '( ' + str(i) + ': ' + str(player[pos].cards[i].name) + ' )\n'
            msgg = '/move ' + str(i)
            buttons.append(types.KeyboardButton(msgg))
        keyboard.add(*buttons)
        unoBot.bot.send_message(player[pos].id, msg)
        unoBot.bot.send_message(unoBot.CHAT_ID, str(player[pos].name) +' выбери номер карты, которую кинешь или возьми из колоды (/move)', reply_markup=keyboard)

        if all(can_put_card(i) == False for i in range(len(player[pos].cards))):
            unoBot.bot.send_message(player[pos].id, 'ну блииин( бери карту   (напиши: /move')
            while player_hasActed[player[pos].name] == False:
                pass
            player_hasActed[player[pos].name] = False

            player[pos].cards.append(take_top_card())
            num = len(player[pos].cards) - 1
            msg = '( '+ str(num) + ': ' + str(player[pos].cards[num].name) +  ' )'
            unoBot.bot.send_message(player[pos].id, msg)
            if can_put_card(num):
                put_card(num)
                unoBot.bot.send_message(unoBot.CHAT_ID, 'урааа карта подошлааа')
            else:
                unoBot.bot.send_message(unoBot.CHAT_ID, 'Лошарик, пропускаешь ход')
                pos = (len(player) + pos + step) % len(player)
        else:
            count_move = 0
            while True:
                while player_hasActed[player[pos].name] == False:
                    pass
                player_hasActed[player[pos].name] = False
                num = player_lastMove[player[pos].name]
                if num == -1:
                    if count_move == 0:
                        player[pos].cards.append(take_top_card())
                        num = len(player[pos].cards) - 1
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'карта добавлена:')
                        msg = '( ' + str(num) + ': ' + str(player[pos].cards[num].name) + ' )'
                        unoBot.bot.send_message(unoBot.CHAT_ID, msg)
                        count_move += 1
                    else:
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'хватит тырить карты из колоды')
                else:
                    if can_put_card(num):
                        put_card(num)
                        break
                    else:
                        unoBot.bot.send_message(unoBot.CHAT_ID, 'Дурачок попробуй ещё')
        if any(len(player[i].cards) == 0 for i in range(len(player))):
            is_playing = False
    unoBot.bot.send_message(unoBot.CHAT_ID, 'Игра закончилась ну блииииин(((09((09(((')
    player = []
    player_hasActed = {}
    player_lastMove = {}
    deck_of_cards = []
    pos = 0
    is_playing = False
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
    cards.append(card(mas[0], mas[1], mas[2], mas[3], mas[4], st))
file.close()

index_in_cards = [i for i in range(len(cards))]
player = []
player_hasActed = {}
player_lastMove = {}
deck_of_cards = []
pos = 0
is_playing = False
