import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram.dispatcher.filters.state import StatesGroup , State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from io import BytesIO
import requests
from PIL import Image
import os
import openai
import cofig as config
import time
import logging
import random
import asyncio
import datetime
from datetime import datetime, timedelta


TOKEN = config.TOKEN
openai.api_key = config.API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db = sqlite3.connect('base.db', check_same_thread=False)
cur = db.cursor()
count_q = 0









ads = [
    "Нужен IELTS? \nВ учебном центре «Stanford» преподаватели с IELTS 8.0\n\nstanfordnukus.t.me",
    "Занимайтесь английским вместе с нами и стройте себе светлое и успешное будущее\n\nstanfordnukus.t.me",
    "Пока другие думают, вы действуйте! \nЗапишитесь на английский \n\nstanfordnukus.t.me",
    "Нужен английский после работы?\nВ учебном центре “Stanford”  идет набор на вечерние курсы😉\n\nstanfordnukus.t.me",
    "Только в учебном центре Stanford можно выиграть Cashback от 1го до 15 миллионов сумов за высокие результаты по IELTS\n\nstanfordnukus.t.me",
    "IELTS kerekpe?\nStanford oqiw orayi mug’allimlerinde  IELTS 8.0😎\n\nstanfordnukus.t.me",
    "Keshki waqit Inglis tili kursi kerekpe?\n\nStanford oqiw orayinda keshki kurslarg’a qabil bolip atir😉\n\nstanfordnukus.t.me",
    "Не теряйте время впустую🙅‍♂️, занимайтесь английским🙆‍♀️ Он понадобится всем!😎😎\n\nstanfordnukus.t.me"
]

messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]

promptHis = []

def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


panel = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
menu1 = types.KeyboardButton("🧑‍💻 Программист 🧑‍💻")
menu2 = types.KeyboardButton("🛎 О нас 🛎")
menu3 = types.KeyboardButton("📊Статистика")
panel.add(menu1,menu2,menu3)






@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global access
    global messages
    global cur
    global db
    await message.answer(f"*Salom {message.from_user.full_name}\nMen ChatGPT, sizga quyidagi imkoniyatlarni taqdim etuvchi sun'iy intellektman:\n•Barcha dasturlash tillarida kod yozish\n•Vazifalarni bajarish\n•Ssenariy yozish\n\nVa boshqa ko'plab imkoniyatlarga egaman!*", parse_mode=types.ParseMode.MARKDOWN, reply_markup=panel)
    with open('chatids.txt','a+') as chatids:
    	print(message.chat.id, file=chatids)
    with open('chatids.txt', 'r') as file:
    	lines = file.readlines()
    	lines = list(set(lines))
    with open('chatids.txt', 'w') as file:
    	file.writelines(lines)

    user_id = message.from_user.id
    name = message.from_user.first_name
    cur.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if cur.fetchone() is None:
    	cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (name, user_id))
    	db.commit()
    	admins = ['6185590222']
    	for i in admins:
    		try:
    			time.sleep(1.5)
    			await bot.send_message(i,f'Yangi foydanaluvchi!\nIsm:[{message.from_user.full_name}](tg://user?id={message.from_user.id})\n🆔️ID:<code>{message.from_user.id}</code>\n🗒Username:@{message.from_user.username}',parse_mode=types.ParseMode.MARKDOWN)
    		except:
    			pass
@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    global messages
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]
    await message.answer("Tarix tozalandi", parse_mode=types.ParseMode.HTML)



@dp.message_handler(commands=['admin'])
async def admin(message):
		admins = ['6185590222']
		if str(message.from_user.id) in admins:
			adm = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
			statistic = types.KeyboardButton("📊Статистика")
			rasslely = types.KeyboardButton("📤Habar yuborish")
			adm.add(statistic,rasslely)
			await bot.send_message(message.chat.id,"👨‍💻Добро пожаловать в панель администратора:",reply_markup=adm)


@dp.message_handler(commands=['send'])
async def rassylka(message):
    admins = ['6185590222']
    if str(message.from_user.id) in admins:
        for i in open('chatids.txt', 'r').readlines():
            time.sleep(0.5)
            await bot.send_message(i,text = message.text.split()[1])

user_messages = {}


@dp.message_handler(content_types=['text'])
async def prompt(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_messages:
        # Check if the time elapsed between the current message and the previous message is less than 5 seconds
        if (datetime.now() - user_messages[user_id]) < timedelta(seconds=5):
            # The user is sending messages too frequently, send a warning message
            await message.answer("Вы отправляете сообщения слишком много раз. Пожалуйста, отправьте повторно через 5 секунд!")
            return
    
    if message.text not in ["/start", "🧑‍💻 Программист 🧑‍💻", "🛎 О нас 🛎", "/clear", "/re", "/admin", "📊Статистика", "📤Habar yuborish", "❌Выйти с админ меню", "/send"]:
        user_messages[user_id] = datetime.now()
        global count_q
        promptHis.append(message.text)
        sent_message = await message.answer("<b>✍️......</b>", parse_mode=types.ParseMode.HTML)
        update(messages, "user", message.text)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages,
        )
        await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        await message.answer(response['choices'][0]['message']['content'], parse_mode="Markdown")
        random_message = random.choice(ads)
        await bot.send_message(message.chat.id, random_message, parse_mode="Markdown")
        count_q += 1
    else:
        if message.text == "📊Статистика":
            global db
            global cur
            cur.execute("SELECT MAX(count) from users")
            t =  cur.fetchone()[0]
            if t is None:
                await bot.send_message(message.chat.id,f"📊Статистика:\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🤖Бот : @DiyarbekAIChatBot\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n👤Количество пользователей : 0\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nКоличество вопросов : {count_q}")
            else:
                await bot.send_message(message.chat.id,f"📊Статистика:\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🤖Бот : @DiyarbekAIChatBot\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n👤Количество пользователей : {t}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nКоличество вопросов : {count_q}")

        elif message.text == "📤Habar yuborish":
            await bot.send_message(message.chat.id,"Habar yuobrish uchun shunaqa qilib yozing /send [yuboriladigon text]")

        elif message.text == "🧑‍💻 Программист 🧑‍💻":
            await bot.send_message(message.chat.id, "Программист: @Diyarbek_Dev\n\nПожалуйста, сообщите разработчику, если вы обнаружите какие-либо технические сбои или ошибки.")
        elif message.text == "🛎 О нас 🛎":
            await bot.send_message(message.chat.id, "Наш канал: @Diyarbek_Blog \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n Наши проекты: @DiyarbekAIChatBot @Awdarmashi_robot @CodeTesterProBot \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n")





if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
