import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
import aiogram.types
from aiogram_broadcaster import MessageBroadcaster
from config import *
from database import *
from aiogram.types.web_app_info import WebAppInfo
from itertools import zip_longest, chain, islice
import tracemalloc
tracemalloc.start()


bot = Bot(token='5748514452:AAH0PsLIEZttWE1mtcidjVpcX6nGL2tNvQs', parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def chunked(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))

class Form(StatesGroup):
    delete_from_favorite = State()

@dp.message_handler(commands='start')
async def start(message):

    add_user(message.chat.id)
    #op = get_op()
    #user_channel_status = await bot.get_chat_member(chat_id=, user_id=user_id)
    #if user_channel_status["status"] != 'left':
    #    pass
    list_favorite = get_favorite(message.chat.id)
    print(list_favorite)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_group in chunked(list_favorite, 2):
        row = []
        for button_name in button_group:
            row.append(KeyboardButton(button_name, web_app=WebAppInfo(url=('https://'+ button_name))))
        keyboard.add(*row)
    keyboard.add('Настройки⚙️')
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAETu-RjzMaVicIvJF-ms45eP7hnxq0T1AAC2A8AAkjyYEsV-8TaeHRrmC0E')
    post = sql.execute("SELECT channel_id, message_id FROM posts WHERE state = 1 ").fetchone()
    print(post)
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=post[0], message_id=post[1])
    await message.reply(start_text, reply_markup = keyboard)


@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def hand_post(message):
    
    if message.sender_chat.id == -1001772264006:
        
        sql.execute('UPDATE posts SET state = 0 WHERE state = 1')
        sql.execute(f'INSERT INTO posts VALUES ({message.sender_chat.id}, {message.message_id}, 1)')
        db.commit()

@dp.message_handler(text='Настройки⚙️')
async def settings(message):
    list_favorite = get_favorite(message.chat.id)
    print(list_favorite)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_group in chunked(list_favorite, 2):
        row = []
        for button_name in button_group:
            row.append(KeyboardButton(button_name))
        keyboard.add(*row)
    keyboard.add('Отмена🚫')
    await bot.send_message(message.chat.id, "Выберите, что вы хотите <b>удалить из избранного👇</b>",reply_markup=keyboard)
    await Form.delete_from_favorite.set()

@dp.message_handler(state=Form.delete_from_favorite)
async def delete_favorite(message, state: FSMContext):
    
    if message.text == 'Отмена🚫':
        list_favorite = get_favorite(message.chat.id)
        print(list_favorite)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for button_group in chunked(list_favorite, 2):
            row = []
            for button_name in button_group:
                row.append(KeyboardButton(button_name, web_app=WebAppInfo(url=('https://'+ button_name))))
            keyboard.add(*row)
        keyboard.add('Настройки⚙️')
        await message.reply('Вы в <b>главном меню</b>⚡️', reply_markup=keyboard)
    else:
        try:
            print(message.text)
            favorite = (sql.execute(f'SELECT favorite FROM users WHERE id = {message.chat.id}').fetchone())[0].split()
            print(favorite)
            favorite.remove(message.text)
            text = ''
            for i in favorite:
                text = text + ' ' + i
            print(text  + 'финальная версия списка')
            sql.execute(f"UPDATE users SET favorite = '{text}' WHERE id = {message.chat.id}")
            db.commit()
            list_favorite = get_favorite(message.chat.id)
            print(list_favorite)
        except:
            pass
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for button_group in chunked(list_favorite, 2):
            row = []
            for button_name in button_group:
                row.append(KeyboardButton(button_name, web_app=WebAppInfo(url=('https://'+ button_name))))
            keyboard.add(*row)
        keyboard.add('Настройки⚙️')
    
        await message.reply('<b>Удалено!</b>🗑', reply_markup=keyboard)
    await state.finish()



@dp.message_handler()
async def get_link(message): 
    
    url = ''
    print(message.text[0:8])
    if message.text[0:8] != 'https://':
        url = 'https://'
    else:
        url = ''
        
    button = InlineKeyboardButton("Перейти", web_app=WebAppInfo(url=(url+message.text)))
    button2 = InlineKeyboardButton('Добавить в избранное', callback_data='ad_favorite')
    kb = InlineKeyboardMarkup().add(button).add(button2)
    await bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы открыть сайт', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'ad_favorite')
async def ad_favorites(callback_query: types.CallbackQuery):

    add_favorite((callback_query.message.reply_markup.inline_keyboard[0][0].web_app.url), callback_query.message.chat.id)
    list_favorite = get_favorite(callback_query.message.chat.id)
    print(list_favorite)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_group in chunked(list_favorite, 2):
        row = []
        for button_name in button_group:
            row.append(KeyboardButton(button_name, web_app=WebAppInfo(url=('https://'+ button_name))))
        keyboard.add(*row)
    keyboard.add('Настройки⚙️')
    #for i in chunked(list_favorite, 2):
    #    keyboard.add(*KeyboardButton(i, web_app=WebAppInfo(url=('https://'+ i))))
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=message_id)

    await bot.send_message(callback_query.message.chat.id, 'Добавлено в избранное', reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)