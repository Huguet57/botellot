from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = '5056375298:AAEvWp2PmwcwzZTxWiGKriDUlAIJp9xLkkg'

def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    with open("/home/andreu/botellot/examples/files/file.pdf", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)


updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader))

updater.start_polling()
updater.idle()