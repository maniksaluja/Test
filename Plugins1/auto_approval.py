from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait, BadRequest  # Add necessary imports
from config import FSUB_1, FSUB_2, JOIN_IMAGE, MUST_VISIT_LINK, TUTORIAL_LINK
from templates import JOIN_MESSAGE
from Database.settings import get_settings
from Database.users import add_user_2
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from .join_leave import get_chats

FSUB = [FSUB_1, FSUB_2]

@Client.on_chat_join_request(filters.chat(FSUB_1))
async def cjr(_: Client, r):
    link = (await get_chats(_))[1].invite_link
    markup = IKM(
      [
        [
          IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=link),
          IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url=MUST_VISIT_LINK)
        ],
        [
          IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)
        ]
      ]
    )
    settings = await get_settings()
    if not settings['auto_approval']:
        return
    await _.approve_chat_join_request(
        r.chat.id,
        r.from_user.id
    )
    if not settings["join"]:
        return
    try:
        if JOIN_IMAGE:
            await _.send_photo(r.from_user.id, JOIN_IMAGE, caption=JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        else:
            await _.send_message(r.from_user.id, JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        await add_user_2(r.from_user.id)
    except UserAlreadyParticipant:
        pass  # Ignore if user is already a participant
    except FloodWait as e:
        print(f"Flood wait error: {e.x} seconds")
        await asyncio.sleep(e.x)
    except BadRequest as e:
        if e.MESSAGE == "400 HIDE_REQUESTER_MISSING":
            print("Hide requester missing, can't approve join request.")
        else:
            print(f"BadRequest error: {e.MESSAGE}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
