from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', '3e9328a5bfde21e60ed3681062621bad6d7a8003')

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
        "I'm a specialised bot for shortening Shortzon links which can help you earn money by just sharing links. \n\n 👁️‍🗨️ Powered by @GroupDcBots")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
      k = await message.reply("**HeLlo Everyone. Send Your Link 1st❕ I Will Send Short Link 👍 \n\n🔰 ʙᴏᴛ ʟɪꜱᴛ 🔰  \n✅ ☞ ᴍᴏᴠɪᴇ ꜱᴇᴀʀᴄʜ ʙᴏᴛ ⭐ ☞ @MediaautoSearchbot \n✅ ☞ ᴅʀᴏᴘʟɪɴᴋ ꜱʜᴏʀᴛ ☞ @Droplinkdcbot ɪɴᴜᴘᴅᴀᴛᴇ \n✅ ☞ Group Manager Bot ☞ @GroupManagerDcBot \n✅ ☞ File 2 Link Bot ☞ @Dcstreamsbot \n✅ ☞ Video Merge Bot ☞ @VideoMergeDcBot \n\n 👁️‍🗨️ Powered by @GroupDcBots")
      If k == True:
      await asyncio.sleep(10)
      await k.delete()

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'❗ Here is your [`{short_link}`]({short_link}) \n\n 〽️ Powered by @GroupDcBots', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://shortzon.com/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]

@Client.on_message(filters.private & filters.command("add"))
async def addApiHandler(bot:Update, msg:Message):
    if await search_user_in_community(bot, msg):
        splitMessage = msg.text.split(' ')
        if len(splitMessage) == 2:
            userid = msg.chat.id
            if not apiExist(userid):
                apiKey = splitMessage[1]
                if await isApiValid(apiKey, bot, msg):
                    addApiKey(apiKey, userid)
                    await msg.reply_text(
                        "<b>Your API Key has been added successfully🥳🥳.</b>",
                        parse_mode = "html"
                    )
            else:
                await msg.reply_text(
                    "<b>Your API Key is already added🤪.</b>",
                    parse_mode = "html"
                )
        else:
            await msg.reply_text(
                "<b>Invalid Command⛔\nSend API Key like this <code>/add APIKEY</code>\n\nIf facing any problem🥲 then ask at😊 @AJPyroVerseGroup</b>",
                parse_mode = "html"
            )
    return

fileName = 'broadcast'

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler(bot:Update, msg:Message):
    try:
        #Extracting Broadcasting Message
        message = msg.text.split('/broadcast ')[1]
    except IndexError:
        await msg.reply_text(
            "<b>Broadcast can't be empty.😒</b>",
            parse_mode = 'html'
        )
    except Exception as e:
        await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    else:
        #Getting User`s Id from Database
        for userid in [document['userid'] for document in collection_api_key.find()]:
            try:
                #Sending Message One By One
                await bot.send_message(userid, message)
            except exceptions.bad_request_400.UserIsBlocked:
                #User Blocked the bot
                pass
            except Exception as e:
                await bot.send_message(Config.OWNER_ID, line_number(fileName, e))
    return

bot.run()
