from os import getenv

API_ID = int(getenv('API_ID', '29321225'))
API_HASH = getenv('API_HASH', '9af2b4ce5315e0222d0b30eba7b0905d')
BOT_TOKEN = getenv('BOT_TOKEN', '6563909840:AAFtJUUvH9zKFUrV79vP5Rh4xUOFLxcVGqE')
BOT_TOKEN_2 = getenv('BOT_TOKEN_2', '7208277760:AAGhIdnbcplS43a1yBlBkF9qQB9hPX5HkXE')

SUDO_USERS = getenv('SUDO_USERS', '6604279354') # Example: '1234 6789'
MONGO_DB_URI = getenv('MONGO_DB_URI', 'mongodb+srv://terasharingbot:Vy3hQFVITnJ4RswM@cluster0.vn1hama.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

DB_CHANNEL_ID = int(getenv('DB_CHANNEL_ID', '-1002119403779'))
DB_CHANNEL_2_ID = int(getenv('DB_CHANNEL_2_ID', '7150728058'))
LOG_CHANNEL_ID = getenv('LOG_CHANNEL_ID', '') # Keep it Empty if no Log Channel  

AUTO_DELETE_TIME = int(getenv('AUTO_DELETE_TIME', '18000')) # Enter time in seconds, keep it 0 for disabling.

FSUB_1 = -1002099961365
FSUB_2 = -1001999286144

MUST_VISIT_LINK = "https://t.me/Utra_XYZ/34"

LINK_GENERATE_IMAGE = getenv('LINK_GENERATE_IMAGE', 'https://graph.org/file/4312b84784d06baa0783f.jpg')

TUTORIAL_LINK = getenv('TUTORIAL_LINK', 'https://t.me/Utra_XYZ/32')

CONNECT_TUTORIAL_LINK = getenv('CONNECT_TUTORIAL_LINK', 'https://t.me/Utra_XYZ/3')
SU_IMAGE = "https://graph.org/file/2342d37844afd1b9b96c0.jpg"
# JOIN

JOIN_MESSAGE = getenv('JOIN_MESSAGE', 'You Joined.')
JOIN_IMAGE = getenv('JOIN_IMAGE', 'https://graph.org/file/015fddf0dbeb03b639647.jpg')

# LEAVE

LEAVE_CAPTION = getenv('LEAVE_CAPTION', 'I Love You.')

# USELESS IMAGE AND MESSAGE

USELESS_MESSAGE = getenv('USELESS_MESSAGE', 'This is useless text.')
USELESS_IMAGE = getenv('USELESS_IMAGE', 'https://graph.org/file/c579032c65d8353e43b0f.jpg')

STICKER_ID = 'CAACAgUAAxkBAAIiHWZjPezFGPWT_87VHnJUaschvGtrAAJtDgACYpoYV06rLlLA8dv_HgQ'

CONTENT_SAVER = True

EXPIRY_TIME = 30 # In days

AUTO_SAVE_CHANNEL_ID = -1002179131802

PHONE_NUMBER_IMAGE = "https://graph.org/file/2821554b6b082eb8741dc.jpg"

WARN_IMAGE = 'https://graph.org/file/c86c68e014e471c1ce729.jpg'

# DO NOT CHANGE BELOW CODES.

SUDO_USERS = [int(x) for x in SUDO_USERS.split()]
        
LOG_CHANNEL_ID = int(LOG_CHANNEL_ID) if LOG_CHANNEL_ID else None