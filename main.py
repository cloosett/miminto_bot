import telebot
import sqlite3
from telebot import types
bot = telebot.TeleBot('6295031831:AAGdNMyVyVbEPUlp6mkK62izJ3Dgmpz037M')

yearsanketa = None
nameanketa = None
mistoanketa = None
statanketa = None

namechange = None
yearschange = None
mistochange = None
statanketa = None

ratings = None
anketa_owner_id = None


admin_id = [889166677]
idupdate = None
nameupdate = None
yearsupdate = None
mistoupdate = None
statupdate = None


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in admin_id:
        bot.send_message(message.chat.id, "Ви увійшли в адмін панель")
        bot.send_message(message.chat.id, 'bot ID (9 number): ')
        bot.register_next_step_handler(message, updateid)
    else:
        bot.send_message(message.chat.id, "Ти не адмін!")

def updateid(message):
    global idupdate
    idupdate = message.text
    if len(idupdate) == 9:
        bot.send_message(message.chat.id, 'bot name:')
    else:
        bot.send_message(message.chat.id, 'id 9 number')
        bot.register_message_handler(message, updateid)
        return
    bot.register_next_step_handler(message, updatename)

def updatename(message):
    global nameupdate
    nameupdate = message.text
    bot.send_message(message.chat.id, 'bot year:')
    bot.register_next_step_handler(message, updateyears)


def updateyears(message):
    global yearsupdate
    yearsupdate = message.text
    if not yearsupdate.isdigit():
        bot.send_message(message.chat.id, 'Будь ласка, введіть вік цифрою.')
        bot.register_next_step_handler(message, updateyears)
        return
    bot.send_message(message.chat.id, 'bot city:')
    bot.register_next_step_handler(message, updatemisto)

def updatemisto(message):
    global mistoupdate
    mistoupdate = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('👦')
    btn2 = types.KeyboardButton('👧')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'bot stat:', reply_markup=markup)
    bot.register_next_step_handler(message, updatestat)
def updatestat(message):
    global statupdate
    statupdate = message.text
    bot.send_message(message.chat.id, 'bot photo:')
    bot.register_next_step_handler(message, updatephoto)



@bot.message_handler(content_types=['photo'])
def updatephoto(message):
    try:
        conn = sqlite3.connect('bibintobot.db')
        cursor = conn.cursor()

        photo = message.photo[-1]
        file_id = photo.file_id

        cursor.execute('INSERT INTO bibintobot (id, name, years, city, stat, photograf) VALUES (?, ?, ?, ?, ?, ?)',
                       (idupdate, nameupdate, yearsupdate, mistoupdate, statupdate, file_id))
        conn.commit()

        cursor.close()
        bot.send_message(message.chat.id, 'Анкета бота готова. Продовжи /start')
    except TypeError:
        bot.send_message(message.chat.id, "Відправте фотографію")

@bot.message_handler(commands=['rozsilka'])
def handle_broadcast(message):
    # Перевірка на адміністратора (або будь-яку іншу перевірку, яку ви потребуєте)
    if message.from_user.id == 889166677:  # Замініть на ваш айді адміністратора
        # Список айді користувачів, яким потрібно надіслати повідомлення
        user_ids = ['5841810263, 738790196, 1282078626, 1215192017, 969154976, 933312481, 889166677, 845289723, 812270609']  # Замініть на фактичні айді

        # Текст повідомлення для розсилки
        message_text = 'Вашу анкету оцінили: Нормально👍'

        for user_id in user_ids:
            bot.send_message(chat_id=user_id, text=message_text)

    else:
        bot.reply_to(message, 'У вас немає дозволу на використання цієї команди.')
# СТВОРЕННЯ ТАБЛИЦІ, ОБРОБНИК КОМАНДИ START
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('bibintobot.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS bibintobot (id INTEGER PRIMARY KEY, name varchar(20), years int, city varchar(50), photograf TEXT, stat varchar(20), rated int, user_id int, rated_by int)')
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Мій профіль👤')
    btn2 = types.KeyboardButton('Оцінювати👀')
    markup.row(btn1,btn2)
    btn3 = types.KeyboardButton('Створити анкету😇')
    btn4 = types.KeyboardButton('Заповнити анкету наново🔁')
    markup.row(btn3, btn4)
    btn5 = types.KeyboardButton('Запросити друга📋')
    markup.row(btn5)
    bot.send_message(message.chat.id, '👋 Вов.., ти попав у Мімінто бот \n\n 📊 Тут ти можеш анонімно оцінювати людей, а вони можуть анонімно оцінювати тебе😉 ', reply_markup=markup)
    bot.register_next_step_handler(message, bibinto)

# ОБРОБНИК КНОПОК
def bibinto(message):
    if message.text == 'Мій профіль👤':
        profileanketa(message)
    if message.text == 'Створити анкету😇':
        conn = sqlite3.connect('bibintobot.db')
        cursor = conn.cursor()

        # Перевірка наявності анкети для користувача
        cursor.execute('SELECT id FROM bibintobot WHERE id = ?', (message.from_user.id,))
        result = cursor.fetchone()

        if result is None:
            bot.send_message(message.chat.id, 'Як до вас звертатись?🤔: ')
            bot.register_next_step_handler(message, anketaname)
        else:
            bot.send_message(message.chat.id, 'Анкета вже створена. Створіть наново.')
            bot.register_next_step_handler(message,bibinto)

        conn.close()
    if message.text == 'Оцінювати👀':
        rating(message)
    if message.text == 'Заповнити анкету наново🔁':
        bot.send_message(message.chat.id, 'Як до вас звертатись?🤔: ')
        bot.register_next_step_handler(message,changename)
    if message.text == 'Запросити друга📋':
        refka(message)
# ПОКАЗ ПРОФІЛЮ

def profile(message):
    conn = sqlite3.connect('bibintobot.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute("SELECT photograf, name, years, city, stat FROM bibintobot WHERE id = ?", (user_id,))
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            file_id, name, years, city, stat = row
            bot.send_photo(message.chat.id, file_id, caption=f'☘️Имя: {name}, {years} років\n\n 🌇Місто: {city} \n\n ⭐Стать: {stat}')
    else:
        bot.send_message(message.chat.id, 'Анкети не знайдено❌, Створіть її😁')
        # Реєстрація обробника наступного кроку після відправки повідомлення "Анкети не знайдено"
        bot.register_next_step_handler(message, bibinto)
        return
    cursor.close()
    conn.close()

    # Оновлення клавіатури після повідомлення "Анкети не знайдено" або відправки повідомлення "Твоя анкета виглядає так👍"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Мій профіль👤')
    btn2 = types.KeyboardButton('Оцінювати👀')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Заповнити анкету наново🔁')
    btn4 = types.KeyboardButton('Запросити друга📋')
    markup.row(btn3,btn4)
    bot.send_message(message.chat.id, 'Твоя анкета виглядає так👍', reply_markup=markup)
    bot.register_next_step_handler(message, bibinto)



def anketaname(message):
    global nameanketa
    nameanketa = message.text
    bot.send_message(message.chat.id, 'Скільки вам років?🤨')
    bot.register_next_step_handler(message, years)

def years(message):
    global yearsanketa
    yearsanketa = message.text
    if not yearsanketa.isdigit():
        bot.send_message(message.chat.id, 'Будь ласка, введіть вік цифрою.')
        bot.register_next_step_handler(message, years)
        return
    bot.send_message(message.chat.id, 'Звідки ви?🌆 ')
    bot.register_next_step_handler(message, statik)

def statik(message):
    global statanketa
    statanketa = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('👦')
    btn2 = types.KeyboardButton('👧')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'Ваша стать👥:', reply_markup=markup)
    bot.register_next_step_handler(message, misto)

def misto(message):
    global mistoanketa
    mistoanketa = message.text
    bot.send_message(message.chat.id, 'Ваше фото📷:')
    bot.register_next_step_handler(message, photografiya)


# ОБРОБНИК ФОТО / І ЗАПОВНЕННЯ ТАБЛИЦІ
@bot.message_handler(content_types=['photo'])
def photografiya(message):
    try:
        conn = sqlite3.connect('bibintobot.db')
        cursor = conn.cursor()
        photo = message.photo[-1]
        file_id = photo.file_id

        cursor.execute(
            'INSERT INTO bibintobot (id, name, years, city, stat, photograf, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (message.from_user.id, nameanketa, yearsanketa, statanketa, mistoanketa, file_id, message.from_user.id))

        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Мій профіль👤')
        btn2 = types.KeyboardButton('Оцінювати👀')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Заповнити анкету наново🔁')
        btn4 = types.KeyboardButton('Запросити друга📋')
        markup.row(btn3,btn4)
        bot.send_message(message.chat.id, 'Ваша анкета готова✔️', reply_markup=markup)
        bot.register_next_step_handler(message, bibinto)
    except TypeError:
        bot.send_message(message.chat.id, "Відправте фотографію")
        bot.register_next_step_handler(message,photografiya)
        return

# Функція для оцінки анкети
def rating(message):
    conn = sqlite3.connect('bibintobot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings
                      (anketa_id INTEGER, user_id INTEGER)''')

    # Перевірка наявності анкети для користувача
    cursor.execute("SELECT id FROM bibintobot WHERE id = ? AND user_id = ?", (message.from_user.id, message.from_user.id))
    row = cursor.fetchone()
    if not row:
        bot.send_message(message.chat.id, 'Щоб оцінювати, створіть анкету.')
        return

    cursor.execute(
        "SELECT id, photograf, name, years, city, stat FROM bibintobot WHERE id NOT IN (SELECT anketa_id FROM ratings WHERE user_id = ?) AND id != ? ORDER BY RANDOM() LIMIT 1",
        (message.from_user.id, message.from_user.id))
    row = cursor.fetchone()
    if row:
        anketa_id, file_id, name, years, city, stat = row
        bot.send_photo(message.chat.id, file_id,
                       caption=f'☘️Ім\'я: {name}, {years} років\n\n ⭐Стать: {stat} \n\n 🌇Місто: {city}')

        # Збереження оцінки користувача для анкети
        cursor.execute("INSERT INTO ratings (anketa_id, user_id) VALUES (?, ?)", (anketa_id, message.from_user.id))
        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Гарно👍')
        btn2 = types.KeyboardButton('Нормально👍')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Погано👎')
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Ваша оцінка🤨:', reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: handle_rating(msg, anketa_id))
    else:
        # Якщо анкети закінчились, відправляємо повідомлення та реєструємо обробник для наступного кроку
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Мій профіль👤')
        btn2 = types.KeyboardButton('Оцінювати👀')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Створити анкету😇')
        btn4 = types.KeyboardButton('Заповнити анкету наново🔁')
        markup.row(btn3, btn4)
        btn5 = types.KeyboardButton('Запросити друга📋')
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Анкет немає, попробуйте пізніше🧐', reply_markup=markup)
        bot.register_next_step_handler(message, bibinto)



def changename(message):
    global namechange
    namechange = message.text
    bot.send_message(message.chat.id, 'Скільки вам років?🤨')
    bot.register_next_step_handler(message, changeyears)

def changeyears(message):
    global yearschange
    yearschange = message.text
    if not yearschange.isdigit():
        bot.send_message(message.chat.id, 'Будь ласка, введіть вік цифрою.')
        bot.register_next_step_handler(message, changeyears)
        return
    bot.send_message(message.chat.id, 'Звідки ви?🌆 ')
    bot.register_next_step_handler(message, сhangestat)

def сhangestat(message):
    global statchange
    statchange = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('👦')
    btn2 = types.KeyboardButton('👧')
    markup.row(btn1,btn2)
    bot.send_message(message.chat.id, 'Ваша стать👥:', reply_markup=markup)
    bot.register_next_step_handler(message, changemisto)


def changemisto(message):
    global mistochange
    mistochange = message.text
    bot.send_message(message.chat.id, 'Ваше фото📷:')
    bot.register_next_step_handler(message,changephoto)

@bot.message_handler(content_types=['photo'])
def changephoto(message):
    try:
        conn = sqlite3.connect('bibintobot.db')
        cursor = conn.cursor()

        photo = message.photo[-1]
        file_id = photo.file_id
        cursor.execute('DELETE FROM bibintobot WHERE id = ?', (message.from_user.id,))
        cursor.execute('INSERT INTO bibintobot (id, name, years, city, stat, photograf) VALUES (?, ?, ?, ?, ?, ?)',
                       (message.from_user.id, namechange, yearschange, statchange, mistochange, file_id))
        conn.commit()

        cursor.close()


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Мій профіль👤')
        btn2 = types.KeyboardButton('Оцінювати👀')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Заповнити анкету наново🔁')
        btn4 = types.KeyboardButton('Запросити друга📋')
        markup.row(btn3,btn4)
        bot.send_message(message.chat.id, 'Ваша анкета готова✔️', reply_markup=markup)
        bot.register_next_step_handler(message, bibinto)
    except TypeError:
        bot.send_message(message.chat.id, "Відправте фотографію")
        bot.register_next_step_handler(message, changephoto)


def handle_rating(message, anketa_id):
    conn = sqlite3.connect('bibintobot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM bibintobot WHERE id = ?", (anketa_id,))
    anketa_owner_name = cursor.fetchone()[0]
    cursor.close()

    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Мій профіль👤')
        btn2 = types.KeyboardButton('Оцінювати👀')
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton('Створити анкету😇')
        btn4 = types.KeyboardButton('Заповнити анкету наново🔁')
        markup.row(btn3, btn4)
        btn5 = types.KeyboardButton('Запросити друга📋')
        markup.row(btn5)
        bot.send_message(anketa_id, f"Вашу анкету оцінили: {message.text}", reply_markup=markup)
        bot.register_next_step_handler(message, bibinto)
    except Exception as e:
        print(e)  # МБ ЧЕРЕЗ ЦЮ ПОМИЛКИ МОЖЕ НА ХОСТИНГ НЕ ЛИТИСЬ

    rating(message)  # Викликаємо функцію rating() для отримання наступної анкети


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Мій профіль👤')
    btn2 = types.KeyboardButton('Оцінювати👀')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Створити анкету😇')
    btn4 = types.KeyboardButton('Заповнити анкету наново🔁')
    markup.row(btn3, btn4)
    btn5 = types.KeyboardButton('Запросити друга📋')
    markup.row(btn5)
    bot.send_message(message.chat.id, 'Головне меню:', reply_markup=markup)
    bot.register_next_step_handler(message, bibinto)


@bot.message_handler(commands=['profile'])
def profileanketa(message):
    conn = sqlite3.connect('bibintobot.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute("SELECT photograf, name, years, city, stat FROM bibintobot WHERE id = ?", (user_id,))
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            file_id, name, years, city, stat = row
            bot.send_photo(message.chat.id, file_id, caption=f'☘️Имя: {name}, {years} років\n\n 🌇Місто: {city} \n\n ⭐Стать: {stat}')
    else:
        bot.send_message(message.chat.id, 'Анкети не знайдено, створіть її😁')
        # Реєстрація обробника наступного кроку після відправки повідомлення "Анкети не знайдено"
        bot.register_next_step_handler(message, bibinto)
        return
    cursor.close()
    conn.close()

    # Оновлення клавіатури після повідомлення "Анкети не знайдено" або відправки повідомлення "Твоя анкета виглядає так👍"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Мій профіль👤')
    btn2 = types.KeyboardButton('Оцінювати👀')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Заповнити анкету наново🔁')
    btn4 = types.KeyboardButton('Запросити друга📋')
    markup.row(btn3,btn4)
    bot.send_message(message.chat.id, 'Твоя анкета виглядає так👍', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bibinto(message)

def refka(message):
    user_id = message.from_user.id
    referral_link = f'https://t.me/MimintoBOT?start={user_id}'
    bot.send_message(message.chat.id, f"Ваше реферальне посилання: {referral_link}")

bot.polling(none_stop=True)

