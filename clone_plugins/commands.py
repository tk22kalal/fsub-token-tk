
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import asyncio
from Script import script
from validators import domain
from clone_plugins.dbusers import db
from clone_plugins.users_api import get_user, update_user_info
from pyrogram import Client, filters, enums
from plugins.database import get_file_details
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import BOT_USERNAME, ADMINS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
from config import PICS, CUSTOM_FILE_CAPTION, AUTO_DELETE_TIME, AUTO_DELETE, PROTECT_CONTENT
import re
import json
import base64
from config import DB_URI as MONGO_URL
from pymongo import MongoClient

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]

logger = logging.getLogger(__name__)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
SECONDS = int(os.getenv("SECONDS", "30"))

async def schedule_deletion(msgs, delay):
    await asyncio.sleep(delay)
    for msg in msgs:
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('MARROW', callback_data='marrow')
        ]]
        me2 = (await client.get_me()).mention
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.CLONE_START_TXT.format(message.from_user.mention, me2),
            reply_markup=reply_markup
        )
        return

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""   

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = '@VJ_Botz  ' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            k = await msg.reply(f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie File/Video will be deleted in <b><u>{AUTO_DELETE} mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>",quote=True)
            await asyncio.sleep(AUTO_DELETE_TIME)
            await msg.delete()
            await k.edit_text("<b>Your File/Video is successfully deleted!!!</b>")
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command('api') & filters.private)
async def shortener_api_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command

    if len(cmd) == 1:
        s = script.SHORTENER_API_MESSAGE.format(base_site=user["base_site"], shortener_api=user["shortener_api"])
        return await m.reply(s)

    elif len(cmd) == 2:    
        api = cmd[1].strip()
        await update_user_info(user_id, {"shortener_api": api})
        await m.reply("Shortener API updated successfully to " + api)
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("base_site") & filters.private)
async def base_site_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command
    text = f"/base_site (base_site)\n\nCurrent base site: None\n\n EX: /base_site shortnerdomain.com"
    
    if len(cmd) == 1:
        return await m.reply(text=text, disable_web_page_preview=True)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        if not domain(base_site):
            return await m.reply(text=text, disable_web_page_preview=True)
        await update_user_info(user_id, {"base_site": base_site})
        await m.reply("Base Site updated successfully")
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('MARROW', callback_data='marrow')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            chat_id=query.message.chat.id, 
            message_id=query.message.id, 
            media=InputMediaPhoto(random.choice(PICS))
        )
        me2 = (await client.get_me()).mention
        await query.message.edit_text(
            text=script.CLONE_START_TXT.format(query.from_user.mention, me2),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "marrow":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomy")],
            [InlineKeyboardButton("OPTHALMOLOGY", callback_data="opthalmology")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)
    
    elif query.data == "anatomy":
        anatomy_buttons = [
            [InlineKeyboardButton("HISTOLOGY", callback_data="histology")],
            [InlineKeyboardButton("UPPER LIMB", callback_data="upper_limb")],
            [InlineKeyboardButton("BACK TO MARROW MENU", callback_data="marrow")]
        ]
        reply_markup = InlineKeyboardMarkup(anatomy_buttons)
        await query.message.edit_reply_markup(reply_markup)
    
    elif query.data == "biochemistry":
        biochemistry_buttons = [
            [InlineKeyboardButton("AMINO ACIDS", callback_data="amino_acids")],
            [InlineKeyboardButton("PROTEINS", callback_data="proteins")],
            [InlineKeyboardButton("BACK TO MARROW MENU", callback_data="marrow")]
        ]
        reply_markup = InlineKeyboardMarkup(biochemistry_buttons)
        await query.message.edit_reply_markup(reply_markup)
    
    elif query.data == "histology":
        bot_username = "testingclonepavo_bot"
        histology_message = (
            f"[<b>⏯: 03. NEET PG 2021 atf.mp4</b>](https://t.me/{bot_username}?start=Z2V0LTg5NjUxMTE5MDM1MzE4Njk)\n\n"
            f"[<b>⏯: 04. NEET PG 2020 atf.mp4</b>](https://t.me/{bot_username}?start=Z2V0LTg5NjYxMTM5Mjc4ODY3OTY)\n\n"
            f"[<b>⏯: 01. INI CET May 2022 atf.mp4</b>](https://t.me/{bot_username}?start=Z2V0LTg5NjcxMTU5NTIyNDE3MjM)"
        )
        msg = await query.message.reply_text(histology_message, protect_content=PROTECT_CONTENT)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data == "upper_limb":
        # Handle upper limb button press if needed
        pass
    
    elif query.data == "amino_acids":
        # Handle amino acids button press if needed
        pass
    
    elif query.data == "proteins":
        # Handle proteins button press if needed
        pass

    
    elif query.data == "opthalmology":
        X = "testingclonepavo_bot"
        histology_message_template = (            
            f"[<b>0.How to approach pediatrics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTA1NjczODMzOTA0NDQ)\n\n"
            f"[<b>1.Normal Newborn</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTE1Njk0MDc3NDUzNzE)\n\n"
            f"[<b>2.Routine Newborn Care</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTI1NzE0MzIxMDAyOTg)\n\n"
            f"[<b>3.Management of LBW Babies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTM1NzM0NTY0NTUyMjU)\n\n"
            f"[<b>4.Neonatal Resuscitation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTQ1NzU0ODA4MTAxNTI)\n\n"
            f"[<b>5.Infections in neonates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTU1Nzc1MDUxNjUwNzk)\n\n"
            f"[<b>6.Birth asphyxia and neonatal seizures</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTY1Nzk1Mjk1MjAwMDY)\n\n"
            f"[<b>7. NEC</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTc1ODE1NTM4NzQ5MzM)\n\n"
            f"[<b>8.Respiratory distress in newborn</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTg1ODM1NzgyMjk4NjA)\n\n"
            f"[<b>9.Neonatal hypoglycemia and infant of diabetic mother</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTk1ODU2MDI1ODQ3ODc)\n\n"
            f"[<b>10.Neonatal jaundice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDA1ODc2MjY5Mzk3MTQ)\n\n"
            f"[<b>11. Normal Growth</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDE1ODk2NTEyOTQ2NDE)\n\n"
            f"[<b>12. Abnormalities in head and size</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDI1OTE2NzU2NDk1Njg)\n\n"
            f"[<b>13. Short stature</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDM1OTM3MDAwMDQ0OTU)\n\n"
            f"[<b>14. Normal development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDQ1OTU3MjQzNTk0MjI)\n\n"
            f"[<b>15.  Disorders of development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDU1OTc3NDg3MTQzNDk)\n\n"
            f"[<b>16. Behavioural disorders in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDY1OTk3NzMwNjkyNzY)\n\n"
            f"[<b>17. Breastfeeding</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDc2MDE3OTc0MjQyMDM)\n\n"
            f"[<b>18. Malnutrition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDg2MDM4MjE3NzkxMzA)\n\n"
            f"[<b>19. Rickets and scurvy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDk2MDU4NDYxMzQwNTc)\n\n"
            f"[<b>20. Genetic disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTA2MDc4NzA0ODg5ODQ)\n\n"
            f"[<b>21. Common childhood infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTE2MDk4OTQ4NDM5MTE)\n\n"
            f"[<b>22. TORCH Infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTI2MTE5MTkxOTg4Mzg)\n\n"
            f"[<b>23. COVID-19 in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTM2MTM5NDM1NTM3NjU)\n\n"
            f"[<b>24. Gastrointestinal anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTQ2MTU5Njc5MDg2OTI)\n\n"
            f"[<b>25. Diarrhoea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTU2MTc5OTIyNjM2MTk)\n\n"
            f"[<b>26. Miscellaneous topics in GIT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTY2MjAwMTY2MTg1NDY)\n\n"
            f"[<b>27. Neonatal Cholestasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTc2MjIwNDA5NzM0NzM)\n\n"
            f"[<b>28. Metabolic Liver Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTg2MjQwNjUzMjg0MDA)\n\n"
            f"[<b>29. Upper airway disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTk2MjYwODk2ODMzMjc)\n\n"
            f"[<b>30. Foreign body, congenital lung anomalies and asthma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjA2MjgxMTQwMzgyNTQ)\n\n"
            f"[<b>31. Lower respiratory tract infection</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjE2MzAxMzgzOTMxODE)\n\n"
            f"[<b>32 . Cystic fibrosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjI2MzIxNjI3NDgxMDg)\n\n"
            f"[<b>33. Fetal circulation and introduction to congenital heart disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjM2MzQxODcxMDMwMzU)\n\n"
            f"[<b>34. Acynotic congenital heart defects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjQ2MzYyMTE0NTc5NjI)\n\n"
            f"[<b>35. Cyanotic congenital heart defects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjU2MzgyMzU4MTI4ODk)\n\n"
            f"[<b>36. Acute rheumatic fever</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjY2NDAyNjAxNjc4MTY)\n\n"
            f"[<b>37. Congenital anomalies of kidney and urinary tract</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjc2NDIyODQ1MjI3NDM)\n\n"
            f"[<b>38. Glomerulonephritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjg2NDQzMDg4Nzc2NzA)\n\n"
            f"[<b>39. Nephrotic syndrome</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjk2NDYzMzMyMzI1OTc)\n\n"
            f"[<b>40. Inherited tubular disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzA2NDgzNTc1ODc1MjQ)\n\n"
            f"[<b>41. Acute kidney injury and chronic kidney disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzE2NTAzODE5NDI0NTE)\n\n"
            f"[<b>42. Congenital anomalies and hydrocephalus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzI2NTI0MDYyOTczNzg)\n\n"
            f"[<b>43. Seizure disorders and epilepsy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzM2NTQ0MzA2NTIzMDU)\n\n"
            f"[<b>44. Cerebral palsy and CNS infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzQ2NTY0NTUwMDcyMzI)\n\n"
            f"[<b>45. Neuromuscular disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzU2NTg0NzkzNjIxNTk)\n\n"
            f"[<b>46. Growth hormone deficiency and hypothyroidism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzY2NjA1MDM3MTcwODY)\n\n"
            f"[<b>47. Adrenal disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzc2NjI1MjgwNzIwMTM)\n\n"
            f"[<b>48. Pubertal disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzg2NjQ1NTI0MjY5NDA)\n\n"
            f"[<b>49. Haematological malignancies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzk2NjY1NzY3ODE4Njc)\n\n"
            f"[<b>50. Solid tumors in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDA2Njg2MDExMzY3OTQ)\n\n"
            f"[<b>51. Rheumatic disease of childhood</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDE2NzA2MjU0OTE3MjE)\n\n"
            f"[<b>52. Approach to anemia in children and nutritional anemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDI2NzI2NDk4NDY2NDg)\n\n"
            f"[<b>53. Congenital Hemolytic Anemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDM2NzQ2NzQyMDE1NzU)\n\n"
            f"[<b>54. Bleeding disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDQ2NzY2OTg1NTY1MDI)\n\n"
            f"[<b>55. Shock</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDU2Nzg3MjI5MTE0Mjk)\n\n"
            f"[<b>56. PALS Guidelines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDY2ODA3NDcyNjYzNTY)\n\n"
        )
        histology_message = histology_message_template.replace("{\"X\"}", X)
        msg = await query.message.reply_text(histology_message, protect_content=PROTECT_CONTENT)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
    






# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
