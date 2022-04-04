from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import filehandling
import messaging
import commands
import callback
import json

# TODO: Crear un fitxer de configuració amb constants privades
config = json.load(open("./config.json"))
BOT_TOKEN = config["BOT_TOKEN"]

updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', commands.start))

updater.dispatcher.add_handler(MessageHandler(Filters.document, filehandling.handlePDF))
updater.dispatcher.add_handler(CallbackQueryHandler(callback.switch))

updater.start_polling()
updater.idle()