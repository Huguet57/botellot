from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from encription import get_hashtag_data
import json

config = json.load(open("./config.json"))
bot = Bot(config["BOT_TOKEN"])

def switch(update: Update, context: CallbackContext) -> None:
    """Handle multiple callbacks"""
    callback_data = update.callback_query.data

    if callback_data == "publish":
        publish_offer(update, context)
        print("Published")
    elif callback_data == "depublish":
        # delete_msg(ticket_id)
        print("Depublished")
    elif callback_data == "reserve":
        private_text(update, context)
        print("Reserved")
    elif callback_data == "buy":
        confirm_buy(update, context)
        print("Bought")

def user(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"@{query.from_user.username} ha seleccionat l'opció.")

# def delete_msg(id: String) -> None:
#     # Get ticket data from id (from database)
#     bot.delete_message(chat_id=config["GROUP_CHAT_ID"], message_id=102) # 102 = message id from database

def publish_offer(update: Update, context: CallbackContext) -> None:
    import messaging
    messaging.send_public_msg(update.callback_query.message)

    responded_msg = update.callback_query.message
    query = update.callback_query
    query.answer()

    keyboard = [[InlineKeyboardButton("Despublicar", callback_data='depublish')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"{responded_msg.text}\n\nEstat: Publicada")
    query.edit_message_reply_markup(reply_markup=reply_markup)

def private_text(update: Update, context: CallbackContext) -> None:
    """Sends a private text to user that has responded"""
    responded_msg = update.callback_query.message
    query = update.callback_query
    query.answer()

    # # Editar missatge públic
    # keyboard = [[InlineKeyboardButton("Agafades.", callback_data='null')]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_reply_markup(reply_markup={})

    # Enviar missatge en privat
    ticket_id = get_hashtag_data(responded_msg.text)
    keyboard = [[InlineKeyboardButton(f"Confirma #{ticket_id}", callback_data='buy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.from_user.send_message(responded_msg.text)
    query.from_user.send_message(f"Confirma que vols l'entrada #{ticket_id} amb aquest botó.", reply_markup=reply_markup)

def confirm_buy(update: Update, context: CallbackContext) -> None:
    """Confirms buy of ticket"""
    responded_msg = update.callback_query.message
    ticket_id = get_hashtag_data(responded_msg.text)
    query = update.callback_query
    query.answer()

    query.edit_message_text(f"Parla amb: @{query.from_user.username} per l'entrada #{ticket_id}.")