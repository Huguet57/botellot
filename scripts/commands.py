def start(update, context) -> None:
    update.message.reply_text("Hola! Envia'm l'entrada que vols vendre en format .pdf")

def publish(update, context) -> None:
    import grouphandling
    grouphandling.send_msg()