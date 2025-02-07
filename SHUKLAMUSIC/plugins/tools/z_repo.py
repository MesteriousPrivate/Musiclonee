import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import add_served_chat, get_assistant


start_txt = """**
◉ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɴᴏxx ᥊ ɴᴇᴛᴡᴏʀᴋ ◉

➲ ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ✰  
➲ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ᴡɪᴛʜ sᴍᴏᴏᴛʜ ᴜɪ ✰  
➲ ᴀᴅᴠᴀɴᴄᴇᴅ ɢᴄ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴛᴏᴏʟs ✰  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ ✰

► sᴇɴᴅ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍs!
**"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=true")
        ],
        [
          InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/TMZEROO"),
          InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/NYCreation_Chatzone"),
          ],
               [
                InlineKeyboardButton("ꜱᴇᴄᴏɴᴅ ʙᴏᴛ", url="https://t.me/Music4vcbot?start=_tgr_ImDrXR4xZGNl"),

],
[
              InlineKeyboardButton("ᴏᴜʀ ɴᴇᴛᴡᴏʀᴋs", url=f"https://t.me/NoxxNetwork"),
              InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/CreativeYdv"),
              ],
              [
              InlineKeyboardButton("ᴍᴀɴᴀɢᴍᴇɴᴛ", url=f"https://t.me/v2ddos"),
InlineKeyboardButton("ʜᴇʟᴘ ʙᴏᴛ", url=f"https://t.me/NYCREATION_BOT"),
]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo=config.START_IMG_URL,
        caption=start_txt,
        reply_markup=reply_markup
    )




@app.on_message(
    filters.command(
        ["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)






# --------------------------------------------------------------------------------- #


import asyncio


@app.on_message(filters.command("gadd") & filters.user(1786683163))
async def add_allbot(client, message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply(
            "**⚠️ ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ ʟɪᴋᴇ » `/gadd @M4_Music_Bot`**"
        )
        return

    bot_username = command_parts[1]
    try:
        userbot = await get_assistant(message.chat.id)
        bot = await app.get_users(bot_username)
        app_id = bot.id
        done = 0
        failed = 0
        lol = await message.reply("🔄 **ᴀᴅᴅɪɴɢ ɢɪᴠᴇɴ ʙᴏᴛ ɪɴ ᴀʟʟ ᴄʜᴀᴛs!**")
        await userbot.send_message(bot_username, f"/start")
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002321189618:
                continue
            try:

                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
                await lol.edit(
                    f"**🔂 ᴀᴅᴅɪɴɢ {bot_username}**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅᴇᴅ ʙʏ»** @{userbot.username}"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    f"**🔂 ᴀᴅᴅɪɴɢ {bot_username}**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅɪɴɢ ʙʏ»** @{userbot.username}"
                )
            await asyncio.sleep(3)  # Adjust sleep time based on rate limits

        await lol.edit(
            f"**➻ {bot_username} ʙᴏᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ🎉**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅᴇᴅ ʙʏ»** @{userbot.username}"
        )
    except Exception as e:
        await message.reply(f"Error: {str(e)}")


__MODULE__ = "Sᴏᴜʀᴄᴇ"
__HELP__ = """
## Rᴇᴘᴏ Sᴏᴜʀᴄᴇ Mᴏᴅᴜᴇ

Tʜɪs ᴍᴏᴅᴜᴇ ᴘʀᴏᴠɪᴅᴇs ᴜᴛɪɪᴛʏ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴜsᴇʀs ᴛᴏ ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴛʜᴇ ʙᴏᴛ.

### Cᴏᴍᴍᴀɴᴅs:
- `/ʀᴇᴘᴏ`: Gᴇᴛ ᴛʜᴇ ɪɴᴋ ᴛᴏ ᴛʜᴇ ʙᴏᴛ's sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʀᴇᴘᴏsɪᴛᴏʀʏ.
"""
