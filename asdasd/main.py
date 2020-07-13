#!venv/bin/python
import logging
import config
import requests
import random
import pyowm
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as BS
logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(types.KeyboardButton(text="Узнать температуру в Ульяновске ⛅"))
    menu_keyboard.add(types.KeyboardButton(text="Бросить кости 🎲"))
    menu_keyboard.add(types.KeyboardButton(text="Вывести случайную цытату 🐒"))
    menu_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Используйте кнопки ниже для взаимодействия с ботом!", reply_markup=menu_keyboard)

#help
@dp.message_handler(commands=["help"])
async def welcome(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Добро пожаловать, <strong>{0.first_name}</strong>! \n\nМеня зовут <b>Бот Олег</b>👨‍🎨 \n\nИ здесь ты можешь узнать: \n•Температуру в Ульяновске ⛅ \n•Бросить кости 🎲 \n•Вывести случайную цытату 🐒\n•Ещё есть секретик 🐷".format(message.from_user), parse_mode='html')
    await message.answer("Введите /start чтобы начать работу 😎")
#секретная команда
@dp.message_handler(commands=["haha"])
async def welcome(message):
    await message.answer("-Купил мужик шляпу, а она ему как раз!\nХЫЫЫЫЫ 🤡")
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBC_5fDIVMCEgu67kXXic4E6on7KAHxAACvAADQGd0EaDuDcNp1xbWGgQ')

# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)

#Погода
@dp.message_handler(content_types=['text'])
async def keyboard_answer(message: types.message):
    if message.chat.type == 'private':
        if message.text == 'Узнать температуру в Ульяновске ⛅':
            #await bot.send_message(message.chat.id, 'Какой город вас интересует🏙?')
            #https://qna.habr.com/q/680230
            city = "Ульяновск"
            print(city)
            owm = pyowm.OWM('517eb41f1720be4a8afc801586d2b54f')  # код погодника API
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place('{},RU'.format(city))
            w = observation.weather
            temperature = w.temperature('celsius')['temp']
            temperature2 = w.detailed_status
            await bot.send_message(message.chat.id, "В городе " + city + " сейчас температура: " + str(temperature) + "°C, " + (str(temperature2)))


        elif message.text == 'Бросить кости 🎲':
            await bot.send_message(message.chat.id, str(random.randint(1, 6)))
        elif message.text == 'Вывести случайную цытату 🐒':
            chitata = 'https://citaty.info/random/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
            full_page = requests.get(chitata, headers=headers)
            soup = BS(full_page.content, 'html.parser')
            convert = soup.findAll("div", {"class": "field-item even last"})[0].text
            await bot.send_message(message.chat.id, "🍀 Случайная цитата 🍀\n\n" + convert)
        else:
            await bot.send_message(message.chat.id, "Я ничего не понимаю 🤯\n\nИспользуй меню для взаимодействия со мной 🤖\n\nИли воспользуйся командами /help или /start 🌚")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)