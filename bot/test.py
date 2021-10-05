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
#     CREATE TABLE IF NOT EXISTS asset_ident (
#         id SERIAL PRIMARY KEY,
#         user_name VARCHAR(255),
#         asset_no BIGINT,
#         asset_name VARCHAR(255),
#         created_at TIMESTAMP WITHOUT TIME ZONE,
#         tele_id INT
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
# --------------------------------------------------------------------------------------------
try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS asset_ident (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        asset_no BIGINT,
        asset_name VARCHAR(255),
        created_at TIMESTAMP WITHOUT TIME ZONE,
        tele_id INT
    );
    """)
    conn.commit();

    print("table1 created")
except:
    print("table1 fail")

try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS asset_in_out (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        asset_no BIGINT,
        location_name VARCHAR(255),
        in_out_exsit VARCHAR(255),
        created_at TIMESTAMP WITHOUT TIME ZONE,
        tele_id INT
    );
    """)
    conn.commit();

    print("table2 created")
except:
    print("table2 fail")

try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS picture (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        picture VARCHAR(255),
        location_name VARCHAR(255),
        explanation VARCHAR(255),
        created_at TIMESTAMP WITHOUT TIME ZONE,
        tele_id INT
    );
    """)
    conn.commit();

    print("table3 created")
except:
    print("table3 fail")

user_data = {}


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.asset_no = int()
        self.asset_name = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Enter Name")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Asset No")
        bot.register_next_step_handler(msg, process_assetno_step)
    except Exception as e:
        bot.reply_to(message, 'oooops1')

def process_assetno_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.asset_no = message.text
        
        msg = bot.send_message(message.chat.id, "Asset Name?")
        bot.register_next_step_handler(msg, process_assetname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops2')
        bot.send_message(message.chat.id, "vvodite chislo")
        bot.register_next_step_handler(send_welcome)

def process_assetname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.asset_name = message.text

        sql = "INSERT INTO asset_ident(user_id,asset_no,asset_name,created_at,tele_id) VALUES(%s, %s, %s, %s, %s)"
        now_time = datetime.datetime.now()
        val = (user.first_name, user.asset_no, user.asset_name, now_time, user_id)

        try:
            cur.execute(sql, val)
            conn.commit();
            print(cur.rowcount, "dannye prinyal")
        except:
            print("dannye fail")
        msg = bot.send_message(message.chat.id, "Succesfull")
    except Exception as e:
        bot.reply_to(message, 'oooops3')


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)

# def process_lastname_step(message):
#     try:
#         user_id = message.from_user.id
#         user = user_data[user_id]
#         user.last_name = message.text
        
#         sql = "INSERT INTO users(first_name,last_name, tele_id, created_at) VALUES(%s, %s, %s, %s)"
#         now_time = datetime.datetime.now()
#         val = (user.first_name, user.last_name, user_id, now_time)

#         try:
#             cur.execute(sql, val)
#             conn.commit();
#             print(cur.rowcount, "dannye prinyal")
#         except:
#             print("dannye fail")
#         msg = bot.send_message(message.chat.id, "vy uspeshno zaregistrirovalis")
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
