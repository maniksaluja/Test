from Database.settings import *
from pyrogram import Client, filters
from config import SUDO_USERS
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from time import time
import asyncio

yes = '☑️'
no = '❌'
auto = '🔄'  # Auto toggle button

def markup(dic):
    mark = IKM(
        [
            [
                IKB('𝘈𝘶𝘵𝘰 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭', callback_data='answer'),
                IKB(yes if dic.get('auto_approval', True) else no, callback_data='toggle_approval')
            ],
            [
                IKB('𝘞𝘦𝘭𝘤𝘰𝘮𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if dic.get('join', True) else no, callback_data='toggle_join')
            ],
            [
                IKB('𝘓𝘦𝘢𝘷𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if dic.get('leave', True) else no, callback_data='toggle_leave')
            ],
            [
                IKB('𝘞𝘢𝘯𝘵 𝘐𝘮𝘢𝘨𝘦', callback_data='answer'),
                IKB(yes if dic.get('image', True) else no, callback_data='toggle_image')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘚𝘢𝘷𝘦', callback_data='answer'),
                IKB(yes if dic.get('auto_save', True) else no, callback_data='toggle_save')
            ],
            [
                IKB('𝘓𝘰𝘨 𝘊𝘩𝘢𝘯𝘯𝘦𝘭', callback_data='answer'),
                IKB(yes if dic.get('logs', True) else no, callback_data='toggle_logs')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦', callback_data='answer'),
                IKB(dic.get('generate', 10), callback_data='toggle_gen')
            ],
            [
                IKB('𝘉𝘓𝘜𝘙 𝘛𝘖𝘎𝘓𝘌', callback_data='answer'),
                IKB(yes if dic.get('blur_enabled', False) else no, callback_data='toggle_blur')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘉𝘓𝘜𝘙', callback_data='answer'),
                IKB(auto if dic.get('blur_auto', False) else no, callback_data='toggle_auto_blur')
            ]
        ]
    )
    return mark

dic = {}

@Client.on_message(filters.command('settings') & filters.user(SUDO_USERS))
async def settings(_, m):
    set = await get_settings()
    txt = '**IT Helps To Change Bot Basic Settings..**'
    mark = markup(set)
    ok = await m.reply(txt, reply_markup=mark)
    dic[m.from_user.id] = [ok, time()]

async def task():
    while True:
        rem = []
        for x in dic:
            if int(time() - dic[x][1]) > 120:
                try:
                    await dic[x][0].delete()
                except:
                    pass
                rem.append(x)
        for y in rem:
            del dic[y]
        await asyncio.sleep(1)

asyncio.create_task(task())

@Client.on_callback_query(filters.regex('toggle_blur'))
async def toggle_blur(_, cq):
    user_data = await get_user_settings(cq.from_user.id)
    blur_enabled = not user_data.get('blur_enabled', False)

    # Update the setting
    await update_user_settings(cq.from_user.id, {'blur_enabled': blur_enabled})

    # Send updated message
    await cq.answer(f"Blur is now {'enabled' if blur_enabled else 'disabled'}.")

    # Updating the buttons
    mark = markup(await get_settings())
    await cq.edit_message_reply_markup(reply_markup=mark)

@Client.on_callback_query(filters.regex('toggle_auto_blur'))
async def toggle_auto_blur(_, cq):
    user_data = await get_user_settings(cq.from_user.id)
    blur_auto = not user_data.get('blur_auto', False)

    # Update the setting
    await update_user_settings(cq.from_user.id, {'blur_auto': blur_auto})

    # Send updated message
    await cq.answer(f"Auto Blur is now {'enabled' if blur_auto else 'disabled'}.")

    # Updating the buttons
    mark = markup(await get_settings())
    await cq.edit_message_reply_markup(reply_markup=mark)
