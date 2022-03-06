from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# TODO: gestionar diferents tipus de callbacks

def switch(update: Update, context: CallbackContext) -> None:
    """Handle multiple callbacks"""
    callback_data = update.callback_query.data

    if callback_data == "publish":
        import grouphandling
        grouphandling.send_public_msg(update.callback_query.message)
        print("Published")
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

def private_text(update: Update, context: CallbackContext) -> None:
    """Sends a private text to user that has responded"""
    responded_msg = update.callback_query.message
    query = update.callback_query
    query.answer()

    # Editar missatge públic
    keyboard = [[InlineKeyboardButton("Agafades.", callback_data='null')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"Entrades agafades per @{query.from_user.username}.")
    query.edit_message_reply_markup(reply_markup=reply_markup)

    # Enviar missatge en privat
    keyboard = [[InlineKeyboardButton("Comprar", callback_data='buy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    buy_msg = "T'has interesat per aquesta entrada:\n\n" + responded_msg.text + "\n\nPaga ara per obtenir-la."
    query.from_user.send_message(buy_msg, reply_markup=reply_markup)

def confirm_buy(update: Update, context: CallbackContext) -> None:
    """Confirms buy of ticket"""
    responded_msg = update.callback_query.message
    query = update.callback_query
    query.answer()

    query.edit_message_text(f"Comprades!")