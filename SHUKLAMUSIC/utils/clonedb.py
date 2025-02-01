from SHUKLAMUSIC.core.mongo import mongodb, pymongodb
from typing import Dict, List, Union

cloneownerdb = mongodb.cloneownerdb
clonebotdb = pymongodb.clonebotdb
clonebotnamedb = mongodb.clonebotnamedb
servedchatdb = mongodb.servedchatdb
serveduserdb = mongodb.serveduserdb


# clone bot owner
async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})


async def get_clonebot_owner(bot_id):
    result = await cloneownerdb.find_one({"bot_id": bot_id})
    if result:
        return result.get("user_id")
    else:
        return False


async def save_clonebot_username(bot_id, user_name):
    await clonebotnamedb.insert_one({"bot_id": bot_id, "user_name": user_name})


async def get_clonebot_username(bot_id):
    result = await clonebotnamedb.find_one({"bot_id": bot_id})
    if result:
        return result.get("user_name")
    else:
        return False


# Served chat
async def add_served_chat_clone(chat_id):
    await servedchatdb.insert_one({"chat_id": chat_id})


async def get_served_chat_clone(chat_id):
    result = await servedchatdb.find_one({"chat_id": chat_id})
    if result:
        return result.get("chat_id")
    else:
        return False


# Served user
async def add_served_user_clone(user_id):
    await serveduserdb.insert_one({"user_id": user_id})


async def get_served_user_clone(user_id):
    result = await serveduserdb.find_one({"user_id": user_id})
    if result:
        return result.get("user_id")
    else:
        return False