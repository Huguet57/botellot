from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

def user(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"@{query.from_user.username} ha seleccionat l'opció.")

def private_text(update: Update, context: CallbackContext) -> None:
    """Sends a private text to user that has responded"""
    query = update.callback_query
    query.answer()

    # Editar missatge públic
    keyboard = [[InlineKeyboardButton("Agafades.", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Missatge enviat a @{query.from_user.username}.")
    query.edit_message_reply_markup(reply_markup=reply_markup)

    # Enviar missatge en privat
    keyboard = [[InlineKeyboardButton("Comprar", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.from_user.send_message("Missatge enviat privadament a l'usuari.", reply_markup=reply_markup)