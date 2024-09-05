#@MxA_Bots | @MovieSeriesArea

import os


class Config(object):
	API_ID = int(os.environ.get("API_ID", "0"))
	API_HASH = os.environ.get("API_HASH")
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	BOT_USERNAME = os.environ.get("BOT_USERNAME")         
	DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-100"))
	BOT_OWNER = int(os.environ.get("BOT_OWNER", "1716234631"))
	DATABASE_URL = os.environ.get("DATABASE_URL")
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "") 
       #UPDATES_CHANNEL_USERNAME = os.environ.get("UPDATES_CHANNEL_USERNAME", "Movies_X_Animes")
	LOG_CHANNEL = os.environ.get("LOG_CHANNEL", None)
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())
	FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "-1001362659779 -1001255795497").split()))
	OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
	ABOUT_BOT_TEXT = f"""𝚃𝚑𝚒𝚜 𝚒𝚜 𝚊 𝙿𝚎𝚛𝚖𝚊𝚗𝚎𝚗𝚝 𝙵𝚒𝚕𝚎𝚂𝚝𝚘𝚛𝚎 𝙱𝚘𝚝. 𝚂𝚎𝚗𝚍 𝙼𝚎 𝚊𝚗𝚢 𝙼𝚎𝚍𝚒𝚊 𝚘𝚛 𝙵𝚒𝚕𝚎. 𝙸 𝚠𝚒𝚕𝚕 𝚊𝚍𝚍 𝚜𝚊𝚟𝚎 𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍 𝙵𝚒𝚕𝚎 𝚒𝚗 𝚖𝚢 𝙳𝚊𝚝𝚊𝚋𝚊𝚜𝚎 𝚊𝚗𝚍 𝚂𝚑𝚊𝚛𝚎 𝚊 𝚂𝚑𝚊𝚛𝚎𝚊𝚋𝚕𝚎 𝙻𝚒𝚗𝚔.\n
╭────[ ⚝ 𝙻𝚞𝚏𝚏𝚢 𝙵𝚒𝚕𝚎𝚜𝚝𝚘𝚛𝚎 𝙱𝚘𝚝 ⚝]────⍟
├🔸🤖 **𝙼𝚢 𝙽𝚊𝚖𝚎:** [𝐋𝐮𝐟𝐟𝐲 𝐅𝐢𝐥𝐞𝐬𝐭𝐨𝐫𝐞 𝐁𝐨𝐭](https://t.me/{BOT_USERNAME})
│
├🔸📝 **𝙻𝚊𝚗𝚐𝚞𝚊𝚐𝚎:** [𝐏𝐲𝐭𝐡𝐨𝐧𝟑](https://www.python.org)
│
├🔹📚 **𝙻𝚒𝚋𝚛𝚊𝚛𝚢:** [𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦](https://docs.pyrogram.org)
│
├🔹📡 **𝙷𝚘𝚜𝚝𝚎𝚍 𝙾𝚗:** [𝐇𝐞𝐫𝐨𝐤𝐮](https://heroku.com)
│
├🔸👨‍💻 **𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛:** **[༺S҈a҈n҈t҈u҈༻](tg://user?id=1716234631)** 
│
├🔹👥 **𝚂𝚞𝚙𝚙𝚘𝚛𝚝:**  [𝐒𝐮𝐩𝐩𝐨𝐫𝐭](tg://user?id=1716234631)
│
├🔸🔔 **𝚄𝚙𝚍𝚊𝚝𝚎𝚜:** [𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/MovieSeriesArea)
│
╰────[ **😇 @MovieSeriesArea 😇**]────⍟"""
	ABOUT_DEV_TEXT = f"""
🧑🏻‍💻 **𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿:** **[༺Ujjωαℓ༻](tg://user?id=2051226979)**
𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐢𝐬 𝐒𝐮𝐩𝐞𝐫 𝐍𝐨𝐨𝐛. 𝐉𝐮𝐬𝐭 𝐋𝐞𝐚𝐫𝐧𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐨𝐭𝐡𝐞𝐫𝐬. 𝐀𝐧𝐝 𝐒𝐞𝐞𝐤𝐢𝐧𝐠 𝐇𝐞𝐥𝐩 𝐅𝐫𝐨𝐦 𝐏𝐫𝐨 𝐂𝐨𝐝𝐞𝐫𝐬\n**@LuffyMovies**
𝐀𝐥𝐬𝐨 𝐫𝐞𝐦𝐞𝐦𝐛𝐞𝐫 𝐭𝐡𝐚𝐭 𝐰𝐞 𝐰𝐢𝐥𝐥 𝐃𝐞𝐥𝐞𝐭𝐞 𝐀𝐝𝐮𝐥𝐭 𝐂𝐨𝐧𝐭𝐞𝐧𝐭𝐬 𝐟𝐫𝐨𝐦 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞. 𝐒𝐨 𝐛𝐞𝐭𝐭𝐞𝐫 𝐝𝐨𝐧'𝐭 𝐒𝐭𝐨𝐫𝐞 𝐓𝐡𝐨𝐬𝐞 𝐊𝐢𝐧𝐝 𝐨𝐟 𝐓𝐡𝐢𝐧𝐠𝐬.
𝐉𝐨𝐢𝐧 **@MovieSeriesArea**"""
	HOME_TEXT = """
Hello, [{}](tg://user?id={})\n\n𝐓𝐡𝐢𝐬 𝐢𝐬 𝐚 𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 **𝐋𝐮𝐟𝐟𝐲 𝐅𝐢𝐥𝐞𝐬𝐭𝐨𝐫𝐞 𝐁𝐨𝐭**
𝐎𝐩𝐞𝐫𝐚𝐭𝐞𝐝 𝐛𝐲 @MovieSeriesArea
"""	
# MxA_Bots
