import telebot
import numpy as np
file = open("UNO cards.txt", 'r')
class card:
    def __init__(self, num, col, step, count_cards, name_of_card):
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


class players:
    def __init__(self, st):
        self.name = st
        self.cards = []


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


def construct_game():
    global player, deck_of_cards, pos, top_of_deck, step
    for i in range(len(player)):
        for j in range(7):
            player[i].cards.append(take_top_card())
    pos = 0
    step = 1
    top_of_deck = take_top_card()

############################################################################## Проблема в неправильном определении возможности положить две карты разных цветов, но разных специальных действий
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
    global player, deck_of_cards, pos, top_of_deck, step
    while True:
        print('верхняя карта:', top_of_deck.name)
        print(player[pos].name, ' выбери номер карты, которую кинешь')
        for i in range(len(player[pos].cards)):
            print('( ', i, ': ', player[pos].cards[i].name, ' )', end = ' ')
        print()
        if all(can_put_card(i) == False for i in range(len(player[pos].cards))):
            print('ну блииин( бери карту   (напиши: взять карту')
            input()
            player[pos].cards.append(take_top_card())
            num = len(player[pos].cards) - 1
            print('( ', num, ': ', player[pos].cards[num].name, ' )', end = ' ')
            print()
            if can_put_card(num):
                put_card(num)
                print('урааа карта подошлааа')
            else:
                print('Лошарик, пропускаешь ход')
                pos = (len(player) + pos + step) % len(player)
        else:
            while True:
                num = int(input())
                if can_put_card(num):
                    put_card(num)
                    break
                else:
                    print('Дурачок попробуй ещё')
        if any(len(player[i].cards) == 0 for i in range(len(player))):
            return


#
cards = []
while True:
    mas = file.readline().strip()
    if not mas:
        break
    mas = mas.split('_')
    cards.append(card(mas[0], mas[1], mas[2], mas[3], mas[4]))
file.close()
index_in_cards = [i for i in range(len(cards))]
player = []
deck_of_cards = []
print('Создай свою игру')
while True:
    print('add <Имя игрока> - добавление нового игрока')
    print('start game - начать игру')
    st = input()
    if st[:3] == 'add':
        player.append(players(st[4:]))
        print('Игрок ' + st[4:] + ' добавлен')
    if st == 'start game':
        break
#
construct_game()
print('Игра началась)))')
game()
print('Игра закончилась ну блииииин(((09((09(((')
