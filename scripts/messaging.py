# -*- coding: utf-8 -*-

import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot
import json

config = json.load(open("./config.json"))
bot = Bot(config["BOT_TOKEN"])

def send_public_msg(msg):
    group_chatID = config["GROUP_CHAT_ID"]    
    reply_markup = {"inline_keyboard":[[{"text": "Reserva-la", "callback_data": "reserve"}]]}
    msg = bot.send_message(chat_id=group_chatID, text=msg.text, reply_markup=reply_markup)
    return msg

def encode_name(name):
    return hashlib.md5(name.encode()).hexdigest()[0:6]

def compose_ticket_msg(data):
    return f"ENTRADA #{encode_name(data['qr'])}\nData: {data['diasetmana']} ({data['date']})\nClub: {data['clubname']}\nPreu: {data['price']}€"

def publish_button(text):
    keyboard = [[InlineKeyboardButton(text, callback_data='publish')]]
    return InlineKeyboardMarkup(keyboard)