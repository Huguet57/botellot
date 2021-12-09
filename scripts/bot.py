from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import filehandling
import commands

BOT_TOKEN = '5056375298:AAEvWp2PmwcwzZTxWiGKriDUlAIJp9xLkkg'

updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', commands.start))
updater.dispatcher.add_handler(MessageHandler(Filters.document, filehandling.handlePDF))

updater.start_polling()
updater.idle()