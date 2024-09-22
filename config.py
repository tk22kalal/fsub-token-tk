# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import logging
import os
from os import getenv, environ
from distutils.util import strtobool
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from Script import script
load_dotenv("config.env")

CLONE_DB_URI = os.environ.get("CLONE_DB_URI", "")
CDB_NAME = os.environ.get("CDB_NAME", "clonevjbotz")
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "vjbotz")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Bot Information

BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # your bot username without @
PICS = (os.environ.get('PICS', 'https://telegra.ph/file/473b7d1f25866692e7c0a.jpg https://telegra.ph/file/473b7d1f25866692e7c0a.jpg')).split() # Bot Start Picture

# Auto Delete Information
AUTO_DELETE = int(os.environ.get("AUTO_DELETE", "30")) # Time in Minutes
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "1800")) # Time in Seconds

SHORTNER_API = os.environ.get("SHORTNER_API", "")
SHORTNER_SITE = os.environ.get("SHORTNER_SITE", "")
X_SHORTNER_API = os.environ.get("X_SHORTNER_API", "")
X_SHORTNER_SITE = os.environ.get("X_SHORTNER_SITE", "")

CUSTOM_FILE_CAPTION = os.environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = os.environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Channel Information
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", ""))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]

# Bot token dari @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
# API ID Anda dari my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

API_ID = int(os.environ.get("API_ID", ""))

# API Hash Anda dari my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

# ID Channel Database
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

CD_CHANNEL = int(os.environ.get("CHANNEL_ID", ""))

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "True") == "True" else False

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

# Custom Repo for updater.
UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", "master")

# Database SQL


#Database MONGO
MONGO_URI = os.environ.get("MONGO_URI", "")
MONGO_NAME = os.environ.get("MONGO_NAME", "")

# ID dari Channel Atau Group Untuk Wajib Subscribenya
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
FORCE_SUB_GROUP = int(os.environ.get("FORCE_SUB_GROUP", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

user_id = message.from_user.id
# Pesan Awalan /start
START_MSG = os.environ.get(
    "START_MESSAGE",
    "JUST CLICK ON OPEN WEBSITE AND GET FREE LECTURES,\n\nJOIN THE WHATSAPP CHANNEL - <a href='https://whatsapp.com/channel/0029Va5goUJKmCPMfqMeso1D'>Click Here</a>\nJOIN MAIN CHANNEL - <a href='https://t.me/mynextpulse'>Click Here</a>\nJOIN BACKUP CHANNEL - <a href='https://t.me/+QiCvb-5pEJU1Mzc1'>Click Here</a>\n\n<b><a href='https://www.google.com/search?q=afrahtafreeh+site&oq=afrahtafreeh+site?user.id={user_id}'>Click on afrahtafreeh(.)site website which is on first or second position on google search.</a></b>",
)
try:
    ADMINS = [int(x) for x in (os.environ.get("ADMINS", "").split())]
except ValueError:
    raise Exception("Daftar Admin Anda tidak berisi User ID Telegram yang valid.")

# Pesan Saat Memaksa Subscribe
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>",
)

# Atur Teks Kustom Anda di sini, Simpan (None) untuk Menonaktifkan Teks Kustom
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Setel True jika Anda ingin Menonaktifkan tombol Bagikan Kiriman Saluran Anda
DISABLE_CHANNEL_BUTTON = strtobool(os.environ.get("DISABLE_CHANNEL_BUTTON", "False"))

ADMINS.append(OWNER_ID)


MULTI_CLIENT = False
name = str(getenv('name', 'filetolinkvjbot'))
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
WORKERS = int(getenv('WORKERS', '4'))
PORT = int(getenv('PORT', 8080))
BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
NO_PORT = bool(getenv('NO_PORT', False))
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
    
else:
    ON_HEROKU = False
FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'.herokuapp.com'
HAS_SSL=bool(getenv('HAS_SSL',False))
if HAS_SSL:
    URL = ""
else:
    URL = ""

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
