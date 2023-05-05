#@MxA_Bots | @iSmartBoi_Ujjwal

import asyncio
from typing import (
    Union
)
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)


async def handle_force_sub(bot: Client, cmd: Message):
    if Config.UPDATES_CHANNEL and Config.UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(Config.UPDATES_CHANNEL)
    elif Config.UPDATES_CHANNEL and (not Config.UPDATES_CHANNEL.startswith("-100")):
        channel_chat_id = Config.UPDATES_CHANNEL
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="𝚂𝚘𝚛𝚛𝚢 𝚂𝚒𝚛, 𝚈𝚘𝚞 𝚊𝚛𝚎 𝚋𝚊𝚗𝚗𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚖𝚎. 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝙷𝚎𝚛𝚎 👉 [𝚂𝚞𝚙𝚙𝚘𝚛𝚝](https://t.me/mrpremium_bot).",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        except Exception as err:
            print(f"Unable to do Force Subscribe to {Config.UPDATES_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**𝙿𝚕𝚎𝚊𝚜𝚎 𝙹𝚘𝚒𝚗 𝙼𝚢 𝚄𝚙𝚍𝚊𝚝𝚎𝚜 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝!**\n\n"
                 "𝙳𝚞𝚎 𝚝𝚘 𝙾𝚟𝚎𝚛𝚕𝚘𝚊𝚍, 𝙾𝚗𝚕𝚢 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 𝚂𝚞𝚋𝚜𝚌𝚛𝚒𝚋𝚎𝚛𝚜 𝚌𝚊𝚗 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝!😎",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("😇 𝙹𝚘𝚒𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 😇", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 𝚁𝚎𝚏𝚛𝚎𝚜𝚑 🔄", callback_data="refreshForceSub")
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="𝚂𝚘𝚖𝚎𝚝𝚑𝚒𝚗𝚐 𝚠𝚎𝚗𝚝 𝚆𝚛𝚘𝚗𝚐. 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝙷𝚎𝚛𝚎 👉 [𝚂𝚞𝚙𝚙𝚘𝚛𝚝](https://t.me/mrpremium_bot).",
            disable_web_page_preview=True
        )
        return 200
    return 200
