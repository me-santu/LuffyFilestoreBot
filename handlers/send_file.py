#@MxA_Bots | @iSmartBoi_Ujjwal

import os
from os import environ
import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

UPDATES_CHANNEL_USERNAME = ("@LuffyMovies")
DELETE_TIME = int(environ.get('DELETE_TIME', 300))#1min=60s , 2min=60×2=120 , 5min=60×5=300 😎🤏
AUTODELETE_MESSAGE = os.getenv("from os import environ", f'''<b>‼️ 𝙵𝚒𝚕𝚎 𝚠𝚒𝚕𝚕 𝚊𝚞𝚝𝚘 𝚍𝚎𝚕𝚎𝚝𝚎 𝚒𝚗 {DELETE_TIME} 𝚜𝚎𝚌𝚘𝚗𝚍𝚜😱\n💡𝙵𝚘𝚛𝚠𝚊𝚛𝚍 𝚒𝚝 𝚝𝚘 𝚜𝚊𝚟𝚎𝚍 𝚖𝚊𝚜𝚜𝚊𝚐𝚎𝚜 𝚘𝚛 𝚊𝚗𝚢𝚠𝚑𝚎𝚛𝚎 𝚋𝚎𝚏𝚘𝚛𝚎 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐.😁\n😇𝙹𝚘𝚒𝚗 @{UPDATES_CHANNEL_USERNAME}</b>''')

async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"{AUTODELETE_MESSAGE}",
            disable_web_page_preview=True, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)


async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)

        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)


async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    await asyncio.sleep(DELETE_TIME)  #1min=60s , 2min=60×2=120 , 5min=60×5=300 😎🤏
    await sent_message.delete()
