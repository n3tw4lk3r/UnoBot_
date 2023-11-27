import telebot
from threading import Thread

from queue_stream import *

bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')

threadsByChatId = {}
st = stream()
q = Thread(target= st.run)
q.start()
