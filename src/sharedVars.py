import telebot
from threading import Thread

from queue_stream import *

threadsByChatId = {}
st = stream()
q = Thread(target= st.run)
q.start()
