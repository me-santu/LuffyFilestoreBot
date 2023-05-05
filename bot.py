#@MxA_Bots | @iSmartBoi_Ujjwal

import os
import asyncio
import traceback
from binascii import (
    Error
)
from pyrogram import (
    Client,
    enums,
    filters
)
from pyrogram.errors import (
    UserNotParticipant,
    FloodWait,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
from configs import Config
from handlers.database import db
from handlers.add_user_to_db import add_user_to_database
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import (
    handle_force_sub,
    get_invite_link
)
from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import (
    save_media_in_channel,
    save_batch_media_in_channel
)

MediaList = {}

Bot = Client(
    name=Config.BOT_USERNAME,
    in_memory=True,
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):

    if cmd.from_user.id in Config.BANNED_USERS:
        await cmd.reply_text("Sorry, You are banned.")
        return
    if Config.UPDATES_CHANNEL is not None:
        back = await handle_force_sub(bot, cmd)
        if back == 400:
            return
    
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await add_user_to_database(bot, cmd)
        await cmd.reply_text(
            Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍷 𝙹𝚘𝚒𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 🍷", url="https://t.me/LuffyMovies")
                    ],
                    [
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙱𝚘𝚝", callback_data="aboutbot"),
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙳𝚎𝚟", callback_data="aboutdevs"),
                        InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎 🚪", callback_data="closeMessage")
                    ],
                    [
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕", url="https://t.me/LuffyMovies"),
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙶𝚛𝚘𝚞𝚙", url="https://t.me/Request_Movies_Webseries")
                    ]
                ]
            )
        )
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await cmd.reply_text(
                    text=f"**Total Files:** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")


@Bot.on_message((filters.document | filters.video | filters.audio) & ~filters.chat(Config.DB_CHANNEL))
async def main(bot: Client, message: Message):

    if message.chat.type == enums.ChatType.PRIVATE:

        await add_user_to_database(bot, message)

        if Config.UPDATES_CHANNEL is not None:
            back = await handle_force_sub(bot, message)
            if back == 400:
                return

        if message.from_user.id in Config.BANNED_USERS:
            await message.reply_text("Sorry, You are banned!\n\nContact here [Support](https://t.me/mrpremium_bot)",
                                     disable_web_page_preview=True)
            return

        if Config.OTHER_USERS_CAN_SAVE_FILE is False:
            return

        await message.reply_text(
            text="**Choose an option from below:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Save in Batch", callback_data="addToBatchTrue")],
                [InlineKeyboardButton("Get Sharable Link", callback_data="addToBatchFalse")]
            ]),
            quote=True,
            disable_web_page_preview=True
        )
    elif message.chat.type == enums.ChatType.CHANNEL:
        if (message.chat.id == int(Config.LOG_CHANNEL)) or (message.chat.id == int(Config.UPDATES_CHANNEL)) or message.forward_from_chat or message.forward_from:
            return
        elif int(message.chat.id) in Config.BANNED_CHAT_IDS:
            await bot.leave_chat(message.chat.id)
            return
        else:
            pass

        try:
            forwarded_msg = await message.forward(Config.DB_CHANNEL)
            file_er_id = str(forwarded_msg.id)
            share_link = f"https://t.me/{Config.BOT_USERNAME}?start=PredatorHackerzZ_{str_to_b64(file_er_id)}"
            CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.id,
                                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                              "Get Sharable Link", url=share_link)]]))
            if message.chat.username:
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
            else:
                private_ch = str(message.chat.id)[4:]
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
        except FloodWait as sl:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(message.chat.id)}` !!",
                disable_web_page_preview=True
            )
        except Exception as err:
            await bot.leave_chat(message.chat.id)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#ERROR_TRACEBACK:\nGot Error from `{str(message.chat.id)}` !!\n\n**Traceback:** `{err}`",
                disable_web_page_preview=True
            )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


@Bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Users in DB:** `{total_users}`",
        quote=True
    )


@Bot.on_message(filters.private & filters.command("ban_user") & filters.user(Config.BOT_OWNER))
async def ban(c: Client, m: Message):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚝𝚘 𝚋𝚊𝚗 𝚊𝚗𝚢 𝚞𝚜𝚎𝚛 𝚏𝚛𝚘𝚖 𝚝𝚑𝚎 𝚋𝚘𝚝.\n\n"
            f"Usage:\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 You misused me.`\n"
            f"𝚃𝚑𝚒𝚜 𝚠𝚒𝚕𝚕 𝚋𝚊𝚗 𝚞𝚜𝚎𝚛 𝚠𝚒𝚝𝚑 𝚒𝚍 `1234567` 𝚏𝚘𝚛 `28` 𝚍𝚊𝚢𝚜 𝚏𝚘𝚛 𝚝𝚑𝚎 𝚛𝚎𝚊𝚜𝚘𝚗 `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"𝙱𝚊𝚗𝚗𝚒𝚗𝚐 𝚞𝚜𝚎𝚛 {user_id} 𝚏𝚘𝚛 {ban_duration} 𝚍𝚊𝚢𝚜 𝚏𝚘𝚛 𝚝𝚑𝚎 𝚛𝚎𝚊𝚜𝚘𝚗 {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"𝚈𝚘𝚞 𝚊𝚛𝚎 𝚋𝚊𝚗𝚗𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚋𝚘𝚝 𝚏𝚘𝚛 **{ban_duration}** 𝚍𝚊𝚢(𝚜) 𝚏𝚘𝚛 𝚝𝚑𝚎 𝚛𝚎𝚊𝚜𝚘𝚗 __{ban_reason}__ \n\n"
                f"**𝙼𝚎𝚜𝚜𝚊𝚐𝚎 𝚏𝚛𝚘𝚖 𝚝𝚑𝚎 𝚊𝚍𝚖𝚒𝚗**"
            )
            ban_log_text += '\n\n𝚄𝚜𝚎𝚛 𝚗𝚘𝚝𝚒𝚏𝚒𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\n𝚄𝚜𝚎𝚛 𝚗𝚘𝚝𝚒𝚏𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚏𝚊𝚒𝚕𝚎𝚍! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"𝙴𝚛𝚛𝚘𝚛 𝚘𝚌𝚌𝚞𝚛𝚛𝚎𝚍! 𝚃𝚛𝚊𝚌𝚎𝚋𝚊𝚌𝚔 𝚐𝚒𝚟𝚎𝚗 𝚋𝚎𝚕𝚘𝚠\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("unban_user") & filters.user(Config.BOT_OWNER))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚝𝚘 𝚞𝚗𝚋𝚊𝚗 𝚊𝚗𝚢 𝚞𝚜𝚎𝚛.\n\n"
            f"𝚄𝚜𝚊𝚐𝚎:\n\n`/unban_user user_id`\n\n"
            f"𝙴𝚐: `/unban_user 1234567`\n"
            f"𝚃𝚑𝚒𝚜 𝚠𝚒𝚕𝚕 𝚞𝚗𝚋𝚊𝚗 𝚞𝚜𝚎𝚛 𝚠𝚒𝚝𝚑 𝚒𝚍 `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"𝚄𝚗𝚋𝚊𝚗𝚗𝚒𝚗𝚐 𝚞𝚜𝚎𝚛 {user_id}"
        try:
            await c.send_message(
                user_id,
                f"𝚈𝚘𝚞𝚛 𝚋𝚊𝚗 𝚠𝚊𝚜 𝚕𝚒𝚏𝚝𝚎𝚍!"
            )
            unban_log_text += '\n\n𝚄𝚜𝚎𝚛 𝚗𝚘𝚝𝚒𝚏𝚒𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\n𝚄𝚜𝚎𝚛 𝚗𝚘𝚝𝚒𝚏𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚏𝚊𝚒𝚕𝚎𝚍! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"𝙴𝚛𝚛𝚘𝚛 𝚘𝚌𝚌𝚞𝚛𝚛𝚎𝚍! 𝚃𝚛𝚊𝚌𝚎𝚋𝚊𝚌𝚔 𝚐𝚒𝚟𝚎𝚗 𝚋𝚎𝚕𝚘𝚠\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("banned_users") & filters.user(Config.BOT_OWNER))
async def _banned_users(_, m: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"𝚃𝚘𝚝𝚊𝚕 𝚋𝚊𝚗𝚗𝚎𝚍 𝚞𝚜𝚎𝚛(𝚜): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)


@Bot.on_message(filters.private & filters.command("clear_batch"))
async def clear_user_batch(bot: Client, m: Message):
    MediaList[f"{str(m.from_user.id)}"] = []
    await m.reply_text("𝙲𝚕𝚎𝚊𝚛𝚎𝚍 𝚢𝚘𝚞𝚛 𝚋𝚊𝚝𝚌𝚑 𝚏𝚒𝚕𝚎𝚜 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢!")


@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):

    cb_data = cmd.data
    if "aboutbot" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝚂𝚘𝚞𝚛𝚌𝚎 𝙲𝚘𝚍𝚎𝚜 𝚘𝚏 𝙱𝚘𝚝",
                                             url="https://te.legra.ph/file/42e9a66c3df08a9c1987a.mp4")
                    ],
                    [
                        InlineKeyboardButton("𝙶𝚘 𝙷𝚘𝚖𝚎", callback_data="gotohome"),
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙳𝚎𝚟", callback_data="aboutdevs")
                    ]
                ]
            )
        )

    elif "aboutdevs" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_DEV_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝚂𝚘𝚞𝚛𝚌𝚎 𝙲𝚘𝚍𝚎𝚜 𝚘𝚏 𝙱𝚘𝚝",
                                             url="https://te.legra.ph/file/42e9a66c3df08a9c1987a.mp4")
                    ],
                    [
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙱𝚘𝚝", callback_data="aboutbot"),
                        InlineKeyboardButton("𝙶𝚘 𝙷𝚘𝚖𝚎", callback_data="gotohome")
                    ]
                ]
            )
        )

    elif "gotohome" in cb_data:
        await cmd.message.edit(
            Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍷 𝙹𝚘𝚒𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 🍷", url="https://t.me/LuffyMovies")
                    ],
                    [
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙱𝚘𝚝", callback_data="aboutbot"),
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙳𝚎𝚟", callback_data="aboutdevs"),
                        InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎 🚪", callback_data="closeMessage")
                    ],
                    [
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕", url="https://t.me/LuffyMovies"),
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙶𝚛𝚘𝚞𝚙", url="https://t.me/Request_Movies_Webseries")
                    ]
                ]
            )
        )

    elif "refreshForceSub" in cb_data:
        if Config.UPDATES_CHANNEL:
            if Config.UPDATES_CHANNEL.startswith("-100"):
                channel_chat_id = int(Config.UPDATES_CHANNEL)
            else:
                channel_chat_id = Config.UPDATES_CHANNEL
            try:
                user = await bot.get_chat_member(channel_chat_id, cmd.message.chat.id)
                if user.status == "kicked":
                    await cmd.message.edit(
                        text="𝚂𝚘𝚛𝚛𝚢 𝚂𝚒𝚛, 𝚈𝚘𝚞 𝚊𝚛𝚎 𝙱𝚊𝚗𝚗𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚖𝚎. 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝙷𝚎𝚛𝚎 👉 [𝚂𝚞𝚙𝚙𝚘𝚛𝚝](https://t.me/mrpremium_bot).",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                invite_link = await get_invite_link(channel_chat_id)
                await cmd.message.edit(
                    text="**𝙸 𝚕𝚒𝚔𝚎 𝚈𝚘𝚞𝚛 𝚂𝚖𝚊𝚛𝚝𝚗𝚎𝚜𝚜 𝙱𝚞𝚝 𝙳𝚘𝚗'𝚝 𝙱𝚎 𝙾𝚟𝚎𝚛𝚜𝚖𝚊𝚛𝚝! 😑**\n\n",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("😇 𝙹𝚘𝚒𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 😇", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 𝚁𝚎𝚏𝚛𝚎𝚜𝚑 🔄", callback_data="refreshmeh")
                            ]
                        ]
                    )
                )
                return
            except Exception:
                await cmd.message.edit(
                    text="𝚂𝚘𝚖𝚎𝚝𝚑𝚒𝚗𝚐 𝚠𝚎𝚗𝚝 𝚆𝚛𝚘𝚗𝚐. 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝙷𝚎𝚛𝚎 👉 [𝚂𝚞𝚙𝚙𝚘𝚛𝚝](https://t.me/mrpremium_bot).",
                    disable_web_page_preview=True
                )
                return
        await cmd.message.edit(
            text=Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕", url="https://t.me/LuffyMovies"),
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎𝚜 𝙶𝚛𝚘𝚞𝚙", url="https://t.me/Request_Movies_Webseries")
                    ],
                    [
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙱𝚘𝚝", callback_data="aboutbot"),
                        InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 𝙳𝚎𝚟", callback_data="aboutdevs")
                    ]
                ]
            )
        )

    elif cb_data.startswith("ban_user_"):
        user_id = cb_data.split("_", 2)[-1]
        if Config.UPDATES_CHANNEL is None:
            await cmd.answer("𝚂𝚘𝚛𝚛𝚢 𝚂𝚒𝚛, 𝚈𝚘𝚞 𝚍𝚒𝚍𝚗'𝚝 𝚂𝚎𝚝 𝚊𝚗𝚢 𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕!", show_alert=True)
            return
        if not int(cmd.from_user.id) == Config.BOT_OWNER:
            await cmd.answer("𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚕𝚕𝚘𝚠𝚎𝚍 𝚝𝚘 𝚍𝚘 𝚝𝚑𝚊𝚝!", show_alert=True)
            return
        try:
            await bot.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
            await cmd.answer("𝚄𝚜𝚎𝚛 𝙱𝚊𝚗𝚗𝚎𝚍 𝚏𝚛𝚘𝚖 𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕!", show_alert=True)
        except Exception as e:
            await cmd.answer(f"𝙲𝚊𝚗'𝚝 𝙱𝚊𝚗 𝙷𝚒𝚖!\n\n𝙴𝚛𝚛𝚘𝚛: {e}", show_alert=True)

    elif "addToBatchTrue" in cb_data:
        if MediaList.get(f"{str(cmd.from_user.id)}", None) is None:
            MediaList[f"{str(cmd.from_user.id)}"] = []
        file_id = cmd.message.reply_to_message.id
        MediaList[f"{str(cmd.from_user.id)}"].append(file_id)
        await cmd.message.edit("𝙵𝚒𝚕𝚎 𝚂𝚊𝚟𝚎𝚍 𝚒𝚗 𝙱𝚊𝚝𝚌𝚑!\n\n"
                               "𝙿𝚛𝚎𝚜𝚜 𝚋𝚎𝚕𝚘𝚠 👇 𝚋𝚞𝚝𝚝𝚘𝚗 𝚝𝚘 𝚐𝚎𝚝 𝚋𝚊𝚝𝚌𝚑 𝚕𝚒𝚗𝚔.",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("𝙶𝚎𝚝 𝙱𝚊𝚝𝚌𝚑 𝙻𝚒𝚗𝚔", callback_data="getBatchLink")],
                                   [InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎 𝙼𝚎𝚜𝚜𝚊𝚐𝚎", callback_data="closeMessage")]
                               ]))

    elif "addToBatchFalse" in cb_data:
        await save_media_in_channel(bot, editable=cmd.message, message=cmd.message.reply_to_message)

    elif "getBatchLink" in cb_data:
        message_ids = MediaList.get(f"{str(cmd.from_user.id)}", None)
        if message_ids is None:
            await cmd.answer("𝙱𝚊𝚝𝚌𝚑 𝙻𝚒𝚜𝚝 𝙴𝚖𝚙𝚝𝚢!", show_alert=True)
            return
        await cmd.message.edit("𝙷𝚎𝚢 𝚍𝚎𝚊𝚛 𝚙𝚕𝚎𝚊𝚜𝚎 𝚠𝚊𝚒𝚝, 𝚐𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝚋𝚊𝚝𝚌𝚑 𝚕𝚒𝚗𝚔 ...")
        await save_batch_media_in_channel(bot=bot, editable=cmd.message, message_ids=message_ids)
        MediaList[f"{str(cmd.from_user.id)}"] = []

    elif "closeMessage" in cb_data:
        await cmd.message.delete(True)

    try:
        await cmd.answer()
    except QueryIdInvalid: pass


Bot.run()
