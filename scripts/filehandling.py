from time import time
from pdfparsing import fillPDFData
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

RAW_FILES_PATH = '/home/andreu/botellot/files/'
TICKETS_PATH = '/home/andreu/botellot/tickets/'

def downloadFile(update, context):
    timestamp = round(time()*1e6)
    with open(RAW_FILES_PATH + f"{timestamp}.pdf", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    return timestamp

def getTicketsData(filename):
    import os
    import qrtools
    from pdf2image import convert_from_path

    qr = qrtools.QR()
    fullpath = RAW_FILES_PATH + f"{filename}.pdf"
    tickets = convert_from_path(fullpath)

    # Parse data from the PDF
    tickets_data = []
    fillPDFData(tickets_data, fullpath)

    for i, ticket in enumerate(tickets):
        # Step 1: Save with temporal name
        prepath = TICKETS_PATH + f"{filename}_{str(i)}.jpg"
        ticket.save(prepath, 'JPEG')
        
        # Step 2: Decode QR and get its data
        qr.decode(filename=prepath)
        tickets_data[i]["qr"] = qr.data

        # Step 3: Change name to QR data
        postpath = TICKETS_PATH + f"{tickets_data[i]['qr']}.jpg"
        os.rename(prepath, postpath)

    return tickets_data

def compose_msg(data):
    return f"[{data['qr']}]\nEntrada pel {data['diasetmana']} ({data['date']})\nClub: {data['clubname']}\nPreu: {data['price']}€"

def handlePDF(update, context):
    # Step 1: Download file
    filename = downloadFile(update, context)

    # Step 2: Get data from PDF
    tickets_data = getTicketsData(filename)

    # Step 3: Reply with data
    for ticket_data in tickets_data:
        msg = compose_msg(ticket_data)

        keyboard = [[InlineKeyboardButton("Demana-te-la", callback_data='0')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, reply_markup=reply_markup)