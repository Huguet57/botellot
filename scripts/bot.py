from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import filehandling
import grouphandling
import commands
import callback

# TODO: Crear un fitxer de configuració amb constants privades
BOT_TOKEN = '5056375298:AAEvWp2PmwcwzZTxWiGKriDUlAIJp9xLkkg'

updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', commands.start))
updater.dispatcher.add_handler(CommandHandler('publicar', commands.publish))
updater.dispatcher.add_handler(MessageHandler(Filters.document, filehandling.handlePDF))
updater.dispatcher.add_handler(CallbackQueryHandler(callback.private_text))

updater.start_polling()
updater.idle()