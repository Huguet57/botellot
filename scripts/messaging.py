import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def encode_name(name):
    return hashlib.md5(name.encode()).hexdigest()[0:20]

def compose_ticket_msg(data):
    return f"[{encode_name(data['qr'])}]\nEntrada pel {data['diasetmana']} ({data['date']})\nClub: {data['clubname']}\nPreu: {data['price']}€"

def publish_button(text):
    keyboard = [[InlineKeyboardButton(text, callback_data='publish')]]
    return InlineKeyboardMarkup(keyboard)