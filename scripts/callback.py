from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from encription import get_hashtag_data
import json
import database

config = json.load(open("./config.json"))
bot = Bot(config["BOT_TOKEN"])

def switch(update: Update, context: CallbackContext) -> None:
    """Handle multiple callbacks"""
    callback_data = update.callback_query.data
    responded_msg = update.callback_query.message
    ticket_id = get_hashtag_data(responded_msg.text)
    
    if callback_data == "publish":
        if not database.is_published(ticket_id):
            publish_offer(update, context)
            print("Published")
        else:
            # Ja s'ha publicat l'entrada
            keyboard = [[InlineKeyboardButton("Ja s'ha publicat.", callback_data='null')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
    elif callback_data == "republish":
        # Erase
        bot.delete_message(chat_id=responded_msg.chat_id, message_id=(responded_msg.message_id+1))
        bot.delete_message(chat_id=responded_msg.chat_id, message_id=responded_msg.message_id)
        database.erase(ticket_id)
        publish_offer(update, context, republish=True)
        print("Republished")
    elif callback_data == "depublish":
        delete_msg(update, context)
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

def delete_msg(update: Update, context: CallbackContext) -> None:
    # Get ticket data from id (from database)
    responded_msg = update.callback_query.message
    ticket_id = get_hashtag_data(responded_msg.text)
    message_id = database.get_message_id(ticket_id)

    try:
        bot.delete_message(chat_id=config["GROUP_CHAT_ID"], message_id=message_id)
        database.depublish(ticket_id)
        
        # Canviar a 'Republicar'
        keyboard = [[InlineKeyboardButton("Republicar", callback_data='publish')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
    except:
        responded_msg.reply_text(f"Error: No s'ha pogut despublicar l'entrada #{ticket_id}. Mira si ja ho està.")

def publish_offer(update: Update, context: CallbackContext, republish=False) -> None:    
    query = update.callback_query
    query.answer()

    import messaging
    msg = messaging.send_public_msg(query.message)

    # Afegir a la database
    import database
    if not republish: database.add_published(query, msg)

    # Canviar a 'Despublicar'
    keyboard = [[InlineKeyboardButton("Despublicar", callback_data='depublish')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.edit_message_reply_markup(reply_markup=reply_markup)
    except:
        pass

def private_text(update: Update, context: CallbackContext) -> None:
    """Sends a private text to user that has responded"""
    responded_msg = update.callback_query.message
    query = update.callback_query
    query.answer()

    # # Editar missatge públic
    query.edit_message_reply_markup(reply_markup={})

    # Enviar missatge en privat
    ticket_id = get_hashtag_data(responded_msg.text)
    confirm_keyboard = [[InlineKeyboardButton(f"Estic interessat en #{ticket_id}", callback_data='buy')]]
    confirm_markup = InlineKeyboardMarkup(confirm_keyboard)
    deny_keyboard = [[InlineKeyboardButton(f"Renuncia a l'entrada.", callback_data='republish')]]
    deny_markup = InlineKeyboardMarkup(deny_keyboard)

    query.from_user.send_message(responded_msg.text, reply_markup=deny_markup)
    query.from_user.send_message(f"Confirma que vols l'entrada #{ticket_id} amb aquest botó.", reply_markup=confirm_markup)

def confirm_buy(update: Update, context: CallbackContext) -> None:
    """Confirms buy of ticket"""
    responded_msg = update.callback_query.message
    ticket_id = get_hashtag_data(responded_msg.text)
    query = update.callback_query
    query.answer()

    username = database.get_publisher_name(ticket_id)

    repeated_username = f"Parla amb: @{username}.\n" * 10
    query.edit_message_text(f"ENTRADA #{ticket_id}\n\n" + repeated_username + "\nSi hi ha cap problema, sempre pots renunciar a l'entrada per tornar-la a publicar.")
    database.sold(ticket_id)