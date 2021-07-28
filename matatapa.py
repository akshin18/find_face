from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
import asyncio
import requests
import json
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

import json
import random
import requests


azlf = 'qwertyuiopasdfghjklzxcvbnm0123456789-'
TOKEN = '1632761595:AAGkjWV8yY6fqB64RcRdRT0aNTCq7pHAfpc'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

con = sqlite3.connect('mata.db')
cur = con.cursor()

@dp.message_handler(lambda message:  '🔍 Поиск' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''Select id from main where id = '{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''INSERT into main VALUES(?,?,?)''',[message.from_user.id,5,''])
        con.commit()
    if cur.execute(f'''SELECT balance from main where id = '{message.from_user.id}' ''').fetchall()[0][0] < 5:
        await message.answer('''⚠️ Недостаточно средств для Поиска
Стоимость 1 поиска = 5 ₽.''')
    else:

        await message.answer('Отправьте фото')



@dp.message_handler(lambda message:  '👤 Мой аккаунт' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''Select id from main where id = '{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''INSERT into main VALUES(?,?,?)''',[message.from_user.id,5,''])
        con.commit()
    a = cur.execute(f'''SELECT balance from main where id = '{message.from_user.id}' ''').fetchall()[0][0]
    await message.answer(f'''🆔 Ваш ID: {message.from_user.id}\nВаш баланс: {a}''')



@dp.message_handler(lambda message:  '💳 Пополнить баланс' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''Select id from main where id = '{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''INSERT into main VALUES(?,?,?)''',[message.from_user.id,5,''])
        con.commit()
    rb1 = InlineKeyboardMarkup()
    rb1.add(InlineKeyboardButton('2 поиска за 14Р Qiwi',callback_data='pay1'))
    rb1.row(InlineKeyboardButton('10 поисков за 50Р Qiwi',callback_data='pay2'),InlineKeyboardButton('20 поисков за 100Р Qiwi',callback_data='pay3'))
    rb1.row(InlineKeyboardButton('30 поисков за 150Р Qiwi',callback_data='pay4'), InlineKeyboardButton('40 поисков за 200Р Qiwi',callback_data='pay5'))
    rb1.add(InlineKeyboardButton('⬅️ Назад', callback_data='nazad'))
    await message.answer('''Стоимость тарифов:
1) 2 поиска за 14 ₽ 🐌
2) 10 поисков за 50 ₽ 🚘
3) 20 поисков за 100 ₽ (бонус +2 поиска) 🚁
4) 30 поисков за 150 ₽ (бонус +3 поиска) ✈️
5) 40 поисков за 200 ₽ (бонус +5 поисков) 🚀
    ''',reply_markup=rb1)


@dp.callback_query_handler(text='nazad')
async def process_start_command(message: types.CallbackQuery):
    try:
        await bot.delete_message(message.message.chat.id,message_id=message.message.message_id)
        await bot.delete_message(message.message.chat.id, message_id=message.message.message_id-1)
    except:
        pass


@dp.callback_query_handler(text_contains='pay')
async def process_start_command(message:types.CallbackQuery):

    if message.data == 'pay1':
        payment = 14
        cur.execute('')
    elif message.data == 'pay2':
        payment = 50
    elif message.data == 'pay3':
        payment = 100
    elif message.data == 'pay4':
        payment = 150
    elif message.data == 'pay5':
        payment = 200
    I_m1 = InlineKeyboardMarkup()
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        await message.delete()
    except:
        pass
    uid = ''.join([random.choice(azlf) for x in range(100)])
    cur.execute(f'''UPDATE main set uid = '{uid}' where id = '{message.from_user.id}' ''')
    con.commit()
    s7 = requests.Session()
    headers = {
        'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImtiNWx2cy0wMCIsInVzZXJfaWQiOiI3OTc3NDA3NjQwOSIsInNlY3JldCI6IjkzODdkOTEyMzQ1MjBiMWNlMmVkMWQzMGEzMTNkNGQ2MjNkZjQ5M2M0MzcwMzczOTdjOWMwZjZmM2FjZDdjYmIifX0=',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    params = {'amount': {'value': f'{payment}',
                         'currency': 'RUB',
                         },
              'comment': 'Оплата подписки',
              'expirationDateTime': '2030-04-13T14:30:00+03:00',
              'customer': {},
              'customFields': {},
              }
    params = json.dumps(params)
    p = s7.put(f'https://api.qiwi.com/partner/bill/v1/bills/{uid}', data=params, headers=headers)
    I_m1.add(types.InlineKeyboardButton('Оплатить', url=p.json()['payUrl'], callback_data='Оплатить'))
    I_m1.add(types.InlineKeyboardButton('Проверить оплату', callback_data=f'hamali{str(payment)}'))
    await message.message.answer('Оплата:', reply_markup=I_m1)


@dp.callback_query_handler(text_contains='hamali')
async def process_start_command(message: types.CallbackQuery):
    uid = cur.execute(f'''Select uid from main where id = '{message.from_user.id}' ''').fetchall()
    payment = message.data.split('hamali')[1]
    if uid != []:
        uid = uid[0][0]
        s7 = requests.Session()
        headers = {
            'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImtiNWx2cy0wMCIsInVzZXJfaWQiOiI3OTc3NDA3NjQwOSIsInNlY3JldCI6IjkzODdkOTEyMzQ1MjBiMWNlMmVkMWQzMGEzMTNkNGQ2MjNkZjQ5M2M0MzcwMzczOTdjOWMwZjZmM2FjZDdjYmIifX0=',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        p = s7.get(f'https://api.qiwi.com/partner/bill/v1/bills/{uid}', headers=headers)
        # print(p.json()['status']['value'])
        if p.json()['status']['value'] == 'PAID':
            cur.execute(f'''UPDATE main set uid = '' where id = '{message.from_user.id}' ''')
            con.commit()
            cur.execute(f'''UPDATE main set balance = balance + {payment} where id = '{message.from_user.id}' ''')
            con.commit()
            await message.message.answer('ОПЛАТА ПРОШЛА УСПЕШНО!!!')
        else:
            await message.message.answer('ОПЛАНА НЕ ПРИШЛА')
    else:
        await message.message.answer('Вы не создали оплату')


@dp.message_handler(commands=['start'])
async def handle_docs_photo(message: types.Message):
    mk1 = ReplyKeyboardMarkup(resize_keyboard=True)
    mk1.add(KeyboardButton('🔍 Поиск'))
    mk1.add(KeyboardButton('💳 Пополнить баланс'))
    mk1.add(KeyboardButton('👤 Мой аккаунт'))
    await message.answer('Добро пожаловать!',reply_markup=mk1)
    if cur.execute(f'''Select id from main where id = '{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''INSERT into main VALUES(?,?,?)''',[message.from_user.id,5,''])
        con.commit()
    else:
        await message.answer('Вы уже зарегестрированы')


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    if cur.execute(f'''Select id from main where id = '{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''INSERT into main VALUES(?,?,?)''',[message.from_user.id,500,''])
        con.commit()
    if cur.execute(f'''SELECT balance from main where id = '{message.from_user.id}' ''').fetchall()[0][0] < -5:
        await message.answer('''⚠️ Недостаточно средств для Поиска
    Стоимость 1 поиска = 5 ₽.''')
    else:


        cur.execute(f'''update main set balance = balance - 5 where id ='{message.from_user.id}' ''')
        con.commit()
        await message.answer('Готовим')
        await message.photo[-1].download('test.jpg')
        a = open('test.jpg', 'rb').read()
        headers = {
            'content-type': 'image/jpeg',
            'referer': 'https://search4faces.com/vk01/index.html',
            'sec-ch-ua': '''"Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"''',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177'
        }
        while True:
            try:
                r = requests.post('https://search4faces.com/upload.php', headers=headers, data=a)
                r = json.loads(r.text)

                if r == {'url': ''}:
                    await message.answer('На этом фото не видно лица!')
                    break
                data = {'query': "vk01", 'source': "vk", 'filename': r['url'], 'boundings': r['boundings'][0]}
                r = requests.post('https://search4faces.com/detect.php', json=data)

                ye = json.loads(r.text)
                for i in ye['faces'][:10]:
                    # print(i[3],i[10],i[12],i[13],i[14],i[18])
                    await message.answer(
                        f'<a href="{i[3]}">ССЫЛКА</a>\nИмя Фамилия: {i[13]} {i[14]}\nПроцент: %{i[10]}\nВозраст: {i[12]}\nДата рождения: {i[18]}',
                        parse_mode="HTML")
                break

            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
#

