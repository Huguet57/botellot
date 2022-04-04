from tokenize import String
from cryptography.fernet import Fernet
import zlib

import json

config = json.load(open("./config.json"))

def generate_key() -> String:
    return Fernet.generate_key().decode()

def encrypt(message: String, key: String) -> String:
    return Fernet(key.encode()).encrypt(message.encode()).decode()

def decrypt(encrypted: String, key: String) -> String:
    return Fernet(key.encode()).decrypt(encrypted.encode()).decode()

def compress(str: String) -> String:
    # return zlib.compress(str.encode())
    return str

def uncompress(str: String) -> String:
    # return zlib.decompress(str.encode()).decode()
    return str

def to_msg(data):
    # """Transforms JSON data to an encrypted string"""
    # return encrypt(json.dumps(data), config["KEY"])
    
    if data["action"] == "publish":
        short_username = compress(data['username'])
        return f"p,{short_username}"

    return "Undefined"

def to_data(msg):
    # """Transforms an encrypted string to JSON data"""
    # return json.loads(decrypt(msg, config["KEY"]))

    action, data = msg.split(",")
    
    if action == "p":
        print(f"Uncompressed: {uncompress(data)}")
        return { "action": "publish", "username": uncompress(data) }

    return {}

def get_hashtag_data(text):
    for word in text.split():
        if len(word) > 1 and word[0] == '#':
            return word[1:]

    return ""

def find_data_in_msg(text):
    from lxml.html.soupparser import fromstring

    # Step 1. Find the <a> tag(s) and its URL
    html = fromstring(text)
    data_container = html.find(attrs={"has-data": "yes"})
    data_msg = data_container['data']

    # Step 2. Recover the data
    data = to_data(data_msg)

    return data