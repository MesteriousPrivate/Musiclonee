import asyncio

from pyrogram import filters, Client
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import InviteRequestSent

from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.utils.database import get_assistant
from SHUKLAMUSIC.utils.shukla_ban import admin_filter

links = {}

# Monitor bot's admin status change
@Client.on_chat_member_updated()
async def auto_join_on_admin_status(client, chat_member_update: ChatMemberUpdated):
    if (
        chat_member_update.new_chat_member.user.id == client.me.id  # Fixed Client.id to client.me.id
        and chat_member_update.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        chat_id = chat_member_update.chat.id
        userbot = await get_assistant(chat_id)
        userbot_id = userbot.id

        # Attempt to invite the assistant automatically
        try:
            if chat_member_update.chat.username:
                await userbot.join_chat(chat_member_update.chat.username)
            else:
                invite_link = await client.create_chat_invite_link(chat_id, expire_date=None)  # Fixed Client.create_chat_invite_link to client.create_chat_invite_link
                await userbot.join_chat(invite_link.invite_link)
            print(f"Assistant joined chat {chat_id} automatically.")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
            except Exception as e:
                print(f"Error approving join request: {e}")
        except Exception as e:
            print(f"Error in auto-joining assistant: {e}")


@Client.on_message(
    filters.group & filters.command(["userbotjoin", "ujoin"]) & ~filters.private
)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    userbot_id = userbot.id
    done = await message.reply("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ**...")
    await asyncio.sleep(1)

    # Check bot's admin status
    chat_member = await client.get_chat_member(chat_id, client.me.id)  # Fixed Client.get_chat_member to client.me.id

    if chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            if message.chat.username:
                await userbot.join_chat(message.chat.username)
            else:
                invite_link = await client.create_chat_invite_link(chat_id, expire_date=None)  # Fixed Client.create_chat_invite_link to client.create_chat_invite_link
                await userbot.join_chat(invite_link.invite_link)
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ.**")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
            except Exception:
                pass
        except Exception as e:
            await done.edit_text(f"**Error:** {e}")
    else:
        await done.edit_text("**ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ.**")

    # Condition 2: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ.**")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
            except Exception:
                pass
        except Exception as e:
            await done.edit_text(str(e))

    # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await client.get_chat_member(chat_id, userbot.id)  # Fixed Client.get_chat_member to client.get_chat_member
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)  # Fixed Client.unban_chat_member to client.unban_chat_member
                await done.edit_text("**ᴀssɪsᴛᴀɴᴛ ɪs ᴜɴʙᴀɴɴɪɴɢ...**")
                await userbot.join_chat(message.chat.username)
                await done.edit_text(
                    "**ᴀssɪsᴛᴀɴᴛ ᴡᴀs ʙᴀɴɴᴇᴅ, ʙᴜᴛ ɴᴏᴡ ᴜɴʙᴀɴɴᴇᴅ, ᴀɴᴅ ᴊᴏɪɴᴇᴅ ᴄʜᴀᴛ ✅**"
                )
            except InviteRequestSent:
                try:
                    await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
                except Exception:
                    pass
            except Exception as e:
                await done.edit_text(
                    "**ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ, ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ʙᴀɴ ᴘᴏᴡᴇʀ ᴀɴᴅ ɪɴᴠɪᴛᴇ ᴜsᴇʀ ᴘᴏᴡᴇʀ ᴏʀ ᴜɴʙᴀɴ ᴀssɪsᴛᴀɴᴛ.**"
                )
        return

    # Condition 4: Group username is not present/group is private, bot is not admin
    if (
        not message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        await done.edit_text("**ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ.**")

    # Condition 5: Group username is not present/group is private, bot is admin
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            try:
                userbot_member = await client.get_chat_member(chat_id, userbot.id)  # Fixed Client.get_chat_member to client.get_chat_member
                if userbot_member.status not in [
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ]:
                    await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴊᴏɪɴᴇᴅ.**")
                    return
            except Exception as e:
                await done.edit_text("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ**.")
                await done.edit_text("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ**...")
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )  # Fixed Client.create_chat_invite_link to client.create_chat_invite_link
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
            except Exception:
                pass
        except Exception as e:
            await done.edit_text(
                f"**➻ ᴀᴄᴛᴜᴀʟʟʏ ɪ ғᴏᴜɴᴅ ᴛʜᴀᴛ ᴍʏ ᴀssɪsᴛᴀɴᴛ ʜᴀs ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ɪɴᴠɪᴛᴇ ɪᴛ.**"
            )

    # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        userbot_member = await client.get_chat_member(chat_id, userbot.id)  # Fixed Client.get_chat_member to client.get_chat_member
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)  # Fixed Client.unban_chat_member to client.unban_chat_member
                await done.edit_text(
                    "**ᴀssɪsᴛᴀɴᴛ ɪs ᴜɴʙᴀɴɴᴇᴅ**\n**ᴛʏᴘᴇ ᴀɢᴀɪɴ:- /userbotjoin.**"
                )
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )  # Fixed Client.create_chat_invite_link to client.create_chat_invite_link
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text(
                    "**ᴀssɪsᴛᴀɴᴛ ᴡᴀs ʙᴀɴɴᴇᴅ, ɴᴏᴡ ᴜɴʙᴀɴɴᴇᴅ, ᴀɴᴅ ᴊᴏɪɴᴇᴅ ᴄʜᴀᴛ✅**"
                )
            except InviteRequestSent:
                try:
                    await client.approve_chat_join_request(chat_id, userbot_id)  # Fixed Client.approve_chat_join_request to client.approve_chat_join_request
                except Exception:
                    pass

            except Exception as e:
                await done.edit_text(
                    f"**➻ ᴀᴄᴛᴜᴀʟʟʏ ɪ ғᴏᴜɴᴅ ᴛʜᴀᴛ ᴍʏ ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ᴜɴʙᴀɴ ɪᴛ.**"
                )
        return


@Client.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await client.send_message(
            message.chat.id, "**✅ ᴜsᴇʀʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs Chat.**"
        )  # Fixed Client.send_message to client.send_message
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["leaveall"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **ᴜsᴇʀʙᴏᴛ** ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs !")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002090474484:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴀʟʟ ɢʀᴏᴜᴘ...**\n\n**ʟᴇғᴛ:** {left} ᴄʜᴀᴛs.\n**ғᴀɪʟᴇᴅ:** {failed} ᴄʜᴀᴛs."
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ...**\n\n**ʟᴇғᴛ:** {left} chats.\n**ғᴀɪʟᴇᴅ:** {failed} chats."
                )
            await asyncio.sleep(3)
    finally:
        await client.send_message(
            message.chat.id,
            f"**✅ ʟᴇғᴛ ғʀᴏᴍ:* {left} chats.\n**❌ ғᴀɪʟᴇᴅ ɪɴ:** {failed} chats.",
        )  # Fixed Client.send_message to client.send_message