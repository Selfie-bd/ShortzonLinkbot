from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', '478179da2efba73db9b2b56171d6a263adeb239d')

bot = Client('Shortzon Link Shortly Bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm a specialised bot for shortening Shortzon links which can help you earn money by just sharing links. \n\n ποΈβπ¨οΈ Powered by @GroupDcBots")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
      await message.reply(
          f"**HeLlo Everyone. Send Your Link 1stβ I Will Send Short Link π \n\nπ° Κα΄α΄ ΚΙͺκ±α΄ π°  \nβ β α΄α΄α΄ Ιͺα΄ κ±α΄α΄Κα΄Κ Κα΄α΄ β­ β @MediaautoSearchbot \nβ β α΄Κα΄α΄ΚΙͺΙ΄α΄ κ±Κα΄Κα΄ β @Droplinkdcbot ΙͺΙ΄α΄α΄α΄α΄α΄α΄ \nβ β Group Manager Bot β @GroupManagerDcBot \nβ β File 2 Link Bot β @Dcstreamsbot \nβ β Video Merge Bot β @VideoMergeDcBot \n\n ποΈβπ¨οΈ Powered by @GroupDcBots")

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'β Here is your [`{short_link}`]({short_link}) \n\n γ½οΈ Powered by @GroupDcBots', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://tnlinks.in/member/tools/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]
bot.run()
