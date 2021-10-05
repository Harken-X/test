import telebot
import psycopg2
import datetime

bot = telebot.TeleBot("1917165003:AAHVznkQ3tLreW0kTWdrEt9bDEP1SjHEm7Q")
try:
    conn = psycopg2.connect("dbname='test_db' host=localhost user='botcarec' password='dbcar'")
    print("database conected")
except:
    print("database not conected")
cur = conn.cursor()

# --------------------------------sozdanie table__
# try:
#     cur.execute("""
#     CREATE TABLE users (
#         id SERIAL PRIMARY KEY,
#         first_name VARCHAR(255),
#         last_name VARCHAR(255)
#     );
#     """)
#     conn.commit();

#     print("table created")
# except:
#     print("table fail")
# --------------------------------dobavlenie table__
# try:
#     cur.execute("INSERT INTO users(first_name,last_name) VALUES(%s, %s)", ('Beka', 'Davlet'))
#     conn.commit();

#     print("dannye prinyal")
# except:
#     print("dannye fail")
# user_data = {}

# # --------------------------------danny prinyal cherez peremennuyu__
# sql = "INSERT INTO users(first_name,last_name) VALUES(%s, %s)"
# val = ('nur', 'oro')

# try:
#     cur.execute(sql, val)
#     conn.commit();

#     print(cur.rowcount, "dannye prinyal")
# except:
#     print("dannye fail")
# --------------------------------mnojestvennoe dobavlenie__
# sql = "INSERT INTO users(first_name,last_name) VALUES(%s, %s)"
# val = [
# ('petya', 'vladov'),
# ('maksim', 'galkin'),
# ('jenya', 'romanov')
# ]
# try:
#     cur.executemany(sql, val)
#     conn.commit();

#     print(cur.rowcount, "dannye prinyal")
# except:
#     print("dannye fail")
# --------------------------------podskazka__


user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Enter last name")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Enter activity")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text
        
        sql = "INSERT INTO users(first_name,last_name, tele_id, created_at) VALUES(%s, %s, %s, %s)"
        now_time = datetime.datetime.now()
        val = (user.first_name, user.last_name, user_id, now_time)

        try:
            cur.execute(sql, val)
            conn.commit();
            print(cur.rowcount, "dannye prinyal")
        except:
            print("dannye fail")
        msg = bot.send_message(message.chat.id, "Succesfull")
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)