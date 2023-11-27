import telebot
import time
import logic
from queue import Queue
from bot_auxilliary import *

class stream:
    def __init__(self):
        self.stream = Queue()

    def put(self, item):
        self.stream.put(item)

    def run(self):
        while True:
            if not self.stream.empty():
                time.sleep(1)
                info = self.stream.get()
                player = info.from_user.username
                text = info.text
                print(text)
                if '/start_game' in text:
                    start_game(info)
                elif '/start' in text:
                    start(info)
                elif '/stats' in text:
                    stats(info)
                elif '/stiker' in text:
                    stiker(info)
                elif '/end_game' in text:
                    end_game(info)
                elif '/admin' in text:
                    admin(info)
                elif '/help_game' in text:
                    help_game(info)
                elif '/help' in text:
                    help(info)
                elif '/join' in text or 'Присоединиться' in text:
                    join(info)
                elif '/play' in text or "Начать игру" in text:
                    play(info)
                elif '/clear' in text:
                    clear()
                elif info.chat.id in logic.games_byId and logic.games_byId[info.chat.id].isRunning and \
                        (info.text == "Взять карту" or info.text == "Пропуск хода") \
                        and logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player:
                    take_card_or_skip(info)
                elif info.chat.id in logic.games_byId and logic.games_byId[info.chat.id].isRunning and \
                        logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player \
                        and any(info.text == logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards[ind].name \
                                for ind in range(len(logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].cards))):
                    put_card(info)
                elif info.chat.id in logic.games_byId and logic.games_byId[info.chat.id].isRunning and \
                        logic.games_byId[info.chat.id].players[logic.games_byId[info.chat.id].current_position].name == player \
                        and logic.games_byId[info.chat.id].next_color is False:
                    change_color(info)