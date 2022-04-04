import json
import os

config = json.load(open("./config.json"))
PUBLISHED_PATH = config["PUBLISHED_PATH"]
SOLD_PATH = config["SOLD_PATH"]

def to_item(id, msg):
    return f"ticket_id={id},message_id={msg.message_id}"

def from_item(str):
    attributes = str.split(',')
    item = {}
    for attribute in attributes:
        key, val = attribute.split("=")
        item[key] = val

    return item

def add_published(msg):
    from encription import get_hashtag_data
    id = get_hashtag_data(msg.text)

    with open(PUBLISHED_PATH + id + ".msg", 'w') as db_item:
        db_item.write(to_item(id, msg))

def is_published(id):
    for file in os.listdir(os.fsencode(PUBLISHED_PATH)):
        if os.fsdecode(file) == id + ".msg":
            return True

    for file in os.listdir(os.fsencode(SOLD_PATH)):
        if os.fsdecode(file) == id + ".msg":
            return True
    
    return False
            
def get_message_id(id):
    for entry in os.scandir(PUBLISHED_PATH):
        with open(entry.path, 'r') as msg:
            item = from_item(msg.read())
            if item["ticket_id"] == id:
                return item["message_id"]

    return "Undefined"

def sold(id):
    # Move from 'Published' to 'Sold'
    os.rename(
        PUBLISHED_PATH + f"{id}.msg",
        SOLD_PATH + f"{id}.msg"
    )

def depublish(id):
    # Remove from 'Published'
    os.remove(PUBLISHED_PATH + f"{id}.msg")

def erase(id):
    # Remove from 'Sold'
    if os.path.exists(SOLD_PATH + f"{id}.msg"): os.remove(SOLD_PATH + f"{id}.msg")
    # Or remove from 'Published'
    if os.path.exists(PUBLISHED_PATH + f"{id}.msg"): os.remove(PUBLISHED_PATH + f"{id}.msg")