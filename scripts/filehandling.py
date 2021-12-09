from time import time
RAW_FILES_PATH = '/home/andreu/botellot/files/'
TICKETS_PATH = '/home/andreu/botellot/tickets/'

def downloadFile(update, context):
    timestamp = round(time()*1e6)
    with open(RAW_FILES_PATH + f"{timestamp}.pdf", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    return timestamp

def getPDFData(filename):
    import os
    import qrtools
    from pdf2image import convert_from_path

    qr = qrtools.QR()
    fullpath = RAW_FILES_PATH + f"{filename}.pdf"
    tickets = convert_from_path(fullpath)

    tickets_data = []

    for i, ticket in enumerate(tickets):
        # Step 0: Add new entry to tickets
        tickets_data.append({})
        data = tickets_data[i]

        # Step 1: Save with temporal name
        prepath = TICKETS_PATH + f"{filename}_{str(i)}.jpg"
        ticket.save(prepath, 'JPEG')
        
        # Step 2: Get ticket data
        # TODO

        # Step 3: Decode QR and get its data
        qr.decode(filename=prepath)
        data["qr"] = qr.data

        # Step 4: Change name to QR data
        postpath = TICKETS_PATH + f"{data['qr']}.jpg"
        os.rename(prepath, postpath)

    return tickets_data

def handlePDF(update, context):
    # Step 1: Download file
    filename = downloadFile(update, context)

    # Step 2: Get data from PDF
    data = getPDFData(filename)

    print(data)