import requests

# https://api.telegram.org/bot/sendMessage" -d "chat_id=&text=my sample text&reply_markup={\"inline_keyboard\":[[{\"text\": \"Button\", \"callback_data\": \"data\"}]]}"

def send_msg():
    
    bot_token = '5056375298:AAEvWp2PmwcwzZTxWiGKriDUlAIJp9xLkkg'
    group_chatID = '-1001580856085'
    sample_markdown_message = '%2Abold%20text%2A%0A_italic%20text_%0A%5Binline%20URL%5D%28http%3A%2F%2Fwww.example.com%2F%29%0A%5Binline%20mention%20of%20a%20user%5D%28tg%3A%2F%2Fuser%3Fid%3D123456789%29%0A%60inline%20fixed-width%20code%60%0A%60%60%60%0Apre-formatted%20fixed-width%20code%20block%0A%60%60%60%0A%60%60%60python%0Apre-formatted%20fixed-width%20code%20block%20written%20in%20the%20Python%20programming%20language%0A%60%60%60'
    bot_message = sample_markdown_message
    reply_markup = '%7B%22inline_keyboard%22%3A%5B%5B%7B%22text%22%3A%20%22Agafar%22%2C%20%22callback_data%22%3A%20%22get%22%7D%5D%5D%7D' # {"inline_keyboard":[[{"text": "Agafar", "callback_data": "get"}]]}

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + group_chatID + '&parse_mode=Markdown&text=' + bot_message + '&reply_markup=' + reply_markup

    response = requests.get(send_text)
    return response.json()
