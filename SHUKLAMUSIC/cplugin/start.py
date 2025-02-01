import time
from time import time
import asyncio
from pyrogram.errors import UserAlreadyParticipant
import random
from pyrogram.errors import UserNotParticipant
from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
import config
from SHUKLAMUSIC.misc import _boot_
from SHUKLAMUSIC.utils import bot_up_time
from SHUKLAMUSIC.plugins.sudo.sudoers import sudoers_list
from SHUKLAMUSIC.utils.database import (
    add_served_chat_clone,
    add_served_user_clone,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from SHUKLAMUSIC.utils.decorators.language import LanguageStart
from SHUKLAMUSIC.utils.formatters import get_readable_time
from SHUKLAMUSIC.utils.inline import help_pannel, private_panel2, start_panel
from config import BANNED_USERS
from strings import get_string
from SHUKLAMUSIC.utils.database import get_assistant
from time import time
import asyncio
from SHUKLAMUSIC.utils.extraction import extract_user


# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5


SHASHANK_PICS = [
"https://graph.org/file/f76fd86d1936d45a63c64.jpg",
"https://graph.org/file/69ba894371860cd22d92e.jpg",
"https://graph.org/file/67fde88d8c3aa8327d363.jpg",
"https://graph.org/file/3a400f1f32fc381913061.jpg",
"https://graph.org/file/a0893f3a1e6777f6de821.jpg",
"https://graph.org/file/5a285fc0124657c7b7a0b.jpg",
"https://graph.org/file/25e215c4602b241b66829.jpg",
"https://graph.org/file/a13e9733afdad69720d67.jpg",
"https://graph.org/file/692e89f8fe20554e7a139.jpg",
"https://graph.org/file/db277a7810a3f65d92f22.jpg",
"https://graph.org/file/a00f89c5aa75735896e0f.jpg",
"https://graph.org/file/f86b71018196c5cfe7344.jpg",
"https://graph.org/file/a3db9af88f25bb1b99325.jpg",
"https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
"https://graph.org/file/84de4b440300297a8ecb3.jpg",
"https://graph.org/file/84e84ff778b045879d24f.jpg",
"https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
"https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
"https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
"https://graph.org/file/37248e7bdff70c662a702.jpg",
"https://graph.org/file/0bfe29d15e918917d1305.jpg",
"https://graph.org/file/16b1a2828cc507f8048bd.jpg",
"https://graph.org/file/e6b01f23f2871e128dad8.jpg",
"https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
"https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
"https://graph.org/file/39d7277189360d2c85b62.jpg",
"https://graph.org/file/5846b9214eaf12c3ed100.jpg",
"https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
"https://graph.org/file/3514efaabe774e4f181f2.jpg",
"https://graph.org/file/eaa3a2602e43844a488a5.jpg",
"https://graph.org/file/b129e98b6e5c4db81c15f.jpg",
"https://graph.org/file/3ccb86d7d62e8ee0a2e8b.jpg",
"https://graph.org/file/df11d8257613418142063.jpg",
"https://graph.org/file/9e23720fedc47259b6195.jpg",
"https://graph.org/file/826485f2d7db6f09db8ed.jpg",
"https://graph.org/file/ff3ad786da825b5205691.jpg",
"https://graph.org/file/52713c9fe9253ae668f13.jpg",
"https://graph.org/file/8f8516c86677a8c91bfb1.jpg",
"https://graph.org/file/6603c3740378d3f7187da.jpg",
"https://graph.org/file/66cb6ec40eea5c4670118.jpg",
"https://graph.org/file/2e3cf4327b169b981055e.jpg",
]


@Client.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client: Client, message: Message, _):

    a = await client.get_me()
    user_id = message.from_user.id
    current_time = time()
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    await add_served_user_clone(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(SHASHANK_PICS),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)

            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, a.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📥 ᴠɪᴅᴇᴏ", callback_data=f"downloadvideo {query}"
                        ),
                        InlineKeyboardButton(
                            text="📥 ᴀᴜᴅɪᴏ", callback_data=f"downloadaudio {query}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🎧 sᴇᴇ ᴏɴ ʏᴏᴜᴛᴜʙᴇ 🎧", url=link),
                    ],
                ]
            )
            await m.delete()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )

    else:
        out = private_panel2(_)
        await message.reply_photo(
            random.choice(SHASHANK_PICS),
            caption=_["c_start_2"].format(message.from_user.mention, a.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )


@Client.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    a = await client.get_me()
    user_id = message.from_user.id
    current_time = time()

    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    out = start_panel(_)
    BOT_UP = await bot_up_time()
    await message.reply_photo(
        random.choice(SHASHANK_PICS),
        caption=_["start_1"].format(a.mention, BOT_UP),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await add_served_chat_clone(message.chat.id)

    # Check if Userbot is already in the group
    try:
        userbot = await get_assistant(message.chat.id)
        message = await message.reply_text(
            f"**ᴄʜᴇᴄᴋɪɴɢ [ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ᴀᴠᴀɪʟᴀʙɪʟɪᴛʏ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ...**"
        )
        is_userbot = await client.get_chat_member(message.chat.id, userbot.id)
        if is_userbot:
            await message.edit_text(
                f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ᴀʟsᴏ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ, ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ sᴏɴɢs.**"
            )
    except Exception as e:
        # Userbot is not in the group, invite it
        try:
            await message.edit_text(
                f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪs ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ, ɪɴᴠɪᴛɪɴɢ...**"
            )
            invitelink = await client.export_chat_invite_link(message.chat.id)
            await asyncio.sleep(1)
            await userbot.join_chat(invitelink)
            await message.edit_text(
                f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪs ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ, ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ sᴏɴɢs.**"
            )
        except Exception as e:
            await message.edit_text(
                f"**ᴜɴᴀʙʟᴇ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ [ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}). ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ɪɴᴠɪᴛᴇ ᴜsᴇʀ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ [ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**"
            )


@Client.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    a = await client.get_me()
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception as e:
                    print(e)
            if member.id == a.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    await client.leave_chat(message.chat.id)
                    return
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            a.mention,
                            f"https://t.me/{a.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    await client.leave_chat(message.chat.id)
                    return

                out = start_panel(_)
                chid = message.chat.id

                try:
                    userbot = await get_assistant(message.chat.id)

                    chid = message.chat.id

                    if message.chat.username:
                        await userbot.join_chat(f"{message.chat.username}")
                        await message.reply_text(
                            f"**My [Assistant](tg://openmessage?user_id={userbot.id}) also entered the chat using the group's username.**"
                        )
                    else:
                        invitelink = await client.export_chat_invite_link(chid)
                        await asyncio.sleep(1)
                        messages = await message.reply_text(
                            f"**Joining my [Assistant](tg://openmessage?user_id={userbot.id}) using the invite link...**"
                        )
                        await userbot.join_chat(invitelink)
                        await messages.delete()
                        await message.reply_text(
                            f"**My [Assistant](tg://openmessage?user_id={userbot.id}) also entered the chat using the invite link.**"
                        )
                except Exception as e:
                    await message.edit_text(
                        f"**Please make me admin to invite my [Assistant](tg://openmessage?user_id={userbot.id}) in this chat.**"
                    )

                await message.reply_photo(
                    random.choice(SHASHANK_PICS),
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        a.mention,
                        message.chat.title,
                        a.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat_clone(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
