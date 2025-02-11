import re
import time
import logging
import asyncio
import threading
import importlib
from sys import argv
from pyrogram import idle
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)
from SHUKLAMUSIC import app
from config import API_ID, API_HASH
from config import LOGGER_ID
from SHUKLAMUSIC import app
from config import OWNER_ID
from SHUKLAMUSIC.misc import SUDOERS
from datetime import datetime
import requests
from SHUKLAMUSIC.utils.database import get_assistant
from SHUKLAMUSIC.utils.decorators.language import language

# Define the clonebotdb
client = MongoClient('mongodb+srv://rebesik896:Nand00000@cluster0.4cewp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['anonmusic']
clonebotdb = db['clonebotdb']

# Define the has_user_cloned_any_bot function
async def has_user_cloned_any_bot(user_id):
    return clonebotdb.find_one({"user_id": user_id}) is not None

# Define the CLONE_LOGGER
CLONE_LOGGER = -1002321189618  # Replace with your actual logger ID


CLONES = set()

C_BOT_DESC = "Wᴀɴᴛ ᴀ ʙᴏᴛ ʟɪᴋᴇ ᴛʜɪs? Cʟᴏɴᴇ ɪᴛ ɴᴏᴡ! ✅\n\nVɪsɪt: @BlossomXMusicBot ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ!\n\n• Uᴘᴅᴀᴛᴇ: @ShrutiBots\n• Sᴜᴘᴘᴏʀᴛ: @NYCREATION_CHATZONE"

C_BOT_COMMANDS = [
    {"command": "/start", "description": "sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ"},
    {"command": "/help", "description": "ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs."},
    {"command": "/play", "description": "sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ."},
    {"command": "/pause", "description": "ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ."},
    {"command": "/resume", "description": "ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ."},
    {"command": "/skip", "description": "sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ."},
    {"command": "/end", "description": "ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ."},
    {"command": "/ping", "description": "ᴄʜᴇᴄᴋ ᴛʜᴇ ᴩɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ."}
]

@app.on_message(filters.command("clone"))
@language
async def clone_txt(client, message, _):
    userbot = await get_assistant(message.chat.id)

    # check user has already clone bot ? -------
    userid = message.from_user.id
    has_already_cbot = await has_user_cloned_any_bot(userid)

    if has_already_cbot:
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("You have already cloned a bot.")
    else:
        pass

    # check user has already clone bot ? -------

    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("Cloning in progress...")
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="SHUKLAMUSIC.cplugin"), 
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id
            c_b_owner_fname = message.from_user.first_name
            c_bot_owner = message.from_user.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text("The provided bot token is invalid or expired.")
            return
        except Exception as e:
            if "database is locked" in str(e).lower():
                await message.reply_text("The database is currently locked.")
            else:
                await mi.edit_text(f"An error occurred: {str(e)}")
            return

        # Proceed with the cloning process
        await mi.edit_text("Bot cloning successful!")
        try:
            await app.send_message(
                CLONE_LOGGER, f"#NewClonedBot\n\nBᴏᴛ:- {bot.mention}\nUsᴇʀɴᴀᴍᴇ: @{bot.username}\nBᴏᴛ ID : `{bot_id}`\n\n**Oᴡɴᴇʀ : [{c_b_owner_fname}](tg://user?id={c_bot_owner})"
            )
            await userbot.send_message(bot.username, "/start")

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": message.from_user.id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
                "channel": "ProBotts",
                "support": "ProBotGc",
                "premium" : True,
                "Date" : False,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)

            #set bot info ----------------------------
            def set_bot_commands():
                url = f"https://api.telegram.org/bot{bot_token}/setMyCommands"

                params = {"commands": C_BOT_COMMANDS}
                response = requests.post(url, json=params)
                print(response.json())

            set_bot_commands()

            # Set bot's "Description" AutoMatically On Every Restart
            def set_bot_desc():
                url = f"https://api.telegram.org/bot{bot_token}/setMyDescription"
                params = {"description": C_BOT_DESC}
                response = requests.post(url, data=params)
                if response.status_code == 200:
                    logging.info(f"Successfully updated Description for bot: {bot_token}")
                else:
                    logging.error(f"Failed to update Description: {response.text}")

            set_bot_desc()

            #set bot info ----------------------------

            await mi.edit_text(f"Bot @{bot.username} cloned successfully!")
        except BaseException as e:
            logging.exception("Error while cloning bot.")
            await mi.edit_text(
                f"⚠️ <b>ᴇʀʀᴏʀ:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @NYcreation_chatzone to get assistance**"
            )
    else:
        await message.reply_text("Please provide the bot token after the /clone command.")


@app.on_message(
    filters.command(
        [
            "delbot",
            "rmbot",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
@language
async def delete_cloned_bot(client, message, _):
    try:
        if len(message.command) < 2:
            await message.reply_text("Please provide the bot token to delete.")
            return

        bot_token = " ".join(message.command[1:])
        await message.reply_text("Deleting the cloned bot...")

        cloned_bot = clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await message.reply_text("Cloned bot deleted successfully.")
            await restart_bots()
            # Call restart function here after successful deletion
        else:
            await message.reply_text("No cloned bot found with the provided token.")
    except Exception as e:
        await message.reply_text("An error occurred while deleting the cloned bot.")
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots...")
        bots = list(clonebotdb.find())
        for bot in bots:
            bot_token = bot["token"]

            # Check if the bot token is valid
            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f"Invalid or expired token for bot: {bot_token}")
                continue  # Skip this bot and move to the next one

            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="SHUKLAMUSIC.cplugin"),
            )
            await ai.start()

            # Set bot's "Description" AutoMatically On Every Restart
            def set_bot_desc():
                url = f"https://api.telegram.org/bot{bot_token}/setMyDescription"
                params = {"description": C_BOT_DESC}
                response = requests.post(url, data=params)
                if response.status_code == 200:
                    logging.info(f"Successfully updated Description for bot: {bot_token}")
                else:
                    logging.error(f"Failed to update Description: {response.text}")

            # set_bot_desc()

            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass
            await asyncio.sleep(5)

        await app.send_message(
            CLONE_LOGGER, "All Cloned Bots Started!"
        )
    except Exception as e:
        logging.exception("Error while restarting bots.")

def schedule_restart():
    while True:
        time.sleep(43200)  # Sleep for 12 hours (43200 seconds)
        asyncio.run(restart_bots())

# Start the background thread to schedule restarts
threading.Thread(target=schedule_restart, daemon=True).start()

@app.on_message(filters.command("clonedinfo") & filters.user(OWNER_ID))
@language
async def list_cloned_bots_info(client, message, _):
    try:
        cloned_bots = list(clonebotdb.find())
        if not cloned_bots:
            await message.reply_text("No cloned bots found.")
            return

        total_clones = len(cloned_bots)
        text = f"**Tᴏᴛᴀʟ Cʟᴏɴᴇᴅ Bᴏᴛs: {total_clones}**\n\n"

        for bot in cloned_bots:
            text += f"**Bᴏᴛ ID:** `{bot['bot_id']}`\n"
            text += f"**Bᴏᴛ Nᴀᴍᴇ:** {bot['name']}\n"
            text += f"**Bᴏᴛ Usᴇʀɴᴀᴍᴇ:** @{bot['username']}\n"
            text += f"**Bᴏᴛ Tᴏᴋᴇɴ:** `{bot['token']}`\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while listing cloned bots.")


@app.on_message(filters.command("delallclone") & filters.user(OWNER_ID))
@language
async def delete_all_cloned_bots(client, message, _):
    try:
        await message.reply_text("Deleting all cloned bots...")

        # Delete all cloned bots from the database
        clonebotdb.delete_many({})

        # Clear the CLONES set
        CLONES.clear()

        await message.reply_text("All cloned bots deleted successfully.")
    except Exception as e:
        await message.reply_text("An error occurred while deleting all cloned bots.")
        logging.exception(e)


@app.on_message(filters.command(["mybot", "mybots"], prefixes=["/", "."]))
@language
async def my_cloned_bots(client, message, _):
    try:
        user_id = message.from_user.id
        cloned_bots = list(clonebotdb.find({"user_id": user_id}))

        if not cloned_bots:
            await message.reply_text("You have not cloned any bots.")
            return

        total_clones = len(cloned_bots)
        text = f"**Yᴏᴜʀ Cʟᴏɴᴇᴅ Bᴏᴛs: {total_clones}**\n\n"

        for bot in cloned_bots:
            text += f"**Bᴏᴛ Nᴀᴍᴇ:** {bot['name']}\n"
            text += f"**Bᴏᴛ Usᴇʀɴᴀᴍᴇ:** @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while fetching your cloned bots.")


@app.on_message(filters.command("cloned") & SUDOERS)
@language
async def list_cloned_bots(client, message, _):
    try:
        cloned_bots = list(clonebotdb.find())
        if not cloned_bots:
            await message.reply_text("No bots have been cloned yet.")
            return

        total_clones = len(cloned_bots)
        text = f"**Tᴏᴛᴀʟ Cʟᴏɴᴇᴅ Bᴏᴛs: `{total_clones}`**\n\n"

        for bot in cloned_bots:
            # Fetch the bot owner's details using their user_id
            owner = await client.get_users(bot['user_id'])

            # Prepare the profile link and first name
            owner_name = owner.first_name
            owner_profile_link = f"tg://user?id={bot['user_id']}"

            text += f"**Bᴏᴛ ID:** `{bot['bot_id']}`\n"
            text += f"**Bᴏᴛ Nᴀᴍᴇ:** {bot['name']}\n"
            text += f"**Bᴏᴛ Usᴇʀɴᴀᴍᴇ:** @{bot['username']}\n"
            text += f"**Oᴡɴᴇʀ:** [{owner_name}]({owner_profile_link})\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while listing cloned bots.")
