import os
import sys
import telebot
from pprint import pprint
from string import Template
import mysql.connector
from mysql.connector import errorcode



# Telegram your token
bot = telebot.TeleBot("1904032990:AAG8lkxJ-wDnncWjtD1NLzMoz_cRaEQzggk")
# Telegram your group id
group_id = -1001164437665

# получить id канала/группы
# print(bot.get_chat('@vladneverovyoutube').id)

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      port="3307",
      database="dbbot"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Что-то не так с вашим именем пользователя или паролем")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("База данных не существует")
    sys.exit()
  else:
    print(err)
    sys.exit()

cursor = db.cursor()

# cursor.execute("CREATE DATABASE dbbot")

# cursor.execute("CREATE TABLE regs (id INT AUTO_INCREMENT PRIMARY KEY, \
# first_name VARCHAR(255), last_name VARCHAR(255), description VARCHAR(255), user_id INT(11))")

# cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, \
# first_name VARCHAR(255), last_name VARCHAR(255), telegram_user_id INT(11) UNIQUE)")

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.photo_id = 0
        self.description = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Введите имя")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        # pprint(vars(message))
        # message.photo[-1].file_id
        # bot.send_photo(group_id, message.photo[-1].file_id)

        msg = bot.send_message(message.chat.id, "Введите фамилию")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, "Отправьте фотографию")
        bot.register_next_step_handler(msg, process_photo_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_photo_step(message):
    try:
        if message.content_type == 'photo':
            user_id = message.from_user.id
            user = user_data[user_id]
            user.photo_id = message.photo[-1].file_id

            msg = bot.send_message(message.chat.id, "Напишите описание")
            bot.register_next_step_handler(msg, process_description_step)
        else:
            bot.reply_to(message, 'Это не фотография, пришлите пожалуйста фото.')
            process_lastname_step(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_description_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.description = message.text

        # Проверка есть ли пользователь в БД
        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()

        # Если нету, то добавить в БД
        if (existsUser == None):
               sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
                                  VALUES (%s, %s, %s)"
               val = (message.from_user.first_name, message.from_user.last_name, user_id)
               cursor.execute(sql, val)

        # Регистрация заявки
        sql = "INSERT INTO regs (first_name, last_name, description, user_id) \
                                  VALUES (%s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.description, user_id)
        cursor.execute(sql, val)
        db.commit()

        # Сохранение фото на сервере
        file_photo = bot.get_file(user.photo_id)
        filename, file_extension = os.path.splitext(file_photo.file_path)

        downloaded_file_photo = bot.download_file(file_photo.file_path)

        src = 'photos/' + user.photo_id + file_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file_photo)

        bot.send_message(message.chat.id, "Вы успешно зарегистрированны!")
        bot.send_message(group_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")
        bot.send_photo(group_id, user.photo_id)

    except Exception as e:
        bot.reply_to(message, 'oooops')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template('$title *$name* \nИмя: *$first_name*\nФамилия: *$last_name* \nОписание: *$description*')

    return t.substitute({
        'title': title,
        'name' : name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'description': user.description
})

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)