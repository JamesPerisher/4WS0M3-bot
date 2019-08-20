import sqlite3
import time



def start():
    global connection, crsr
    connection = sqlite3.connect("data/users.db")
    crsr = connection.cursor()

def close():
    global connection, crsr
    try:
        connection.commit()
    except:
        pass
    connection.close()

def commit():
    global connection, crsr
    connection.commit()






def create_users_table():
    global connection, crsr
    sql_command = """CREATE TABLE IF NOT EXISTS chat_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username STRING,
    chat_level INTEGER,
    colour VARCHAR(8),
    renewals INTEGER,
    end_date INTEGER);"""
    crsr.execute(sql_command)

def add(user_id, chat_level, colour, end_date):
    if not ifRecord(str(user_id)):
        sql_command = "INSERT INTO chat_users VALUES (NULL, \"%s\", %s, \"%s\", 0, %s);" %(user_id, chat_level, colour, end_date)
        crsr.execute(sql_command)

def renew(user_id, end_date):
    if not ifRecord(str(user_id)):
        sql_command = "UPDATE chat_users SET end_date = %s WHERE user_id = \"%s\";" %(end_date, user_id)
        crsr.execute(sql_command)

        sql_command = "UPDATE chat_users SET renewals = renewals + 1 WHERE user_id = \"%s\";"%(user_id)
        crsr.execute(sql_command)

def new_level(user_id, chat_level):
    if not ifRecord(str(user_id)):
        sql_command = "UPDATE chat_users SET chat_level = \"%s\" WHERE user_id = \"%s\";"%(chat_level, user_id)
        crsr.execute(sql_command)

def get_user(user_id):
    sql_command = "SELECT * FROM chat_users WHERE user_id = \"%s\";"%user_id
    crsr.execute(sql_command)
    return crsr.fetchall()

def ifRecord(user_id):
    global connection, crsr
    sql_command = "SELECT COUNT(1) FROM chat_users WHERE user_id = \"%s\";"%user_id
    crsr.execute(sql_command)
    if crsr.fetchall()[0][0] == 0:
        return False
    return True

def get_chat(user_id):
    user = get_user(user_id)
    if not len(user) == 1:
        print("chat_user error not 1 user: %s"%str(user))
        return (False,None,None)
    user = user[0]
    if user[2] == 0:
        return (True, "#ffffff", None)
    if user[2] == 1:
        return (True, user[3], None)
    if user[2] == 2:
        return (True, user[3], "GREEN")
    if user[2] == 3:
        return (True, user[3], "ALL")
    print("chat_user error invalid permission value: %s"%str(user))
    return (False,None,None)


def change_colour(user_id, colour):
    sql_command = "UPDATE chat_users  SET colour = \"%s\" WHERE user_id = \"%s\"" %(colour, user_id)
    crsr.execute(sql_command)

def change_username(user_id, username):
    sql_command = "UPDATE chat_users  SET username = \"%s\" WHERE user_id = \"%s\"" %(username.replace("\\", ""), user_id)
    crsr.execute(sql_command)


def parse(data):
    if data == None or data == "":
        return None
    if data[1].strip() == "":
        return None

    if data[0]:
        return ("#ff7700", data[1])

    sp = data[1].split(">")
    user = sp[0].split("<")
    message = ">".join(sp[1::])
    if len(user) == 2:
        if message[1] == ">":
            return ("#076108", "**<%s> **%s" %(user[1], message))
        else:
            return ("#1f2999", "**<%s> **%s" %(user[1], message))

    if data[1].split(" ")[1] == "whispers:":
        if not ">" in data[1].split(" ")[0]:
            return ("#a900e3", data[1])
    if " ".join(data[1].split(" ")[1::]) == "joined the game":
        if not ">" in data[1].split(" ")[0]:
            return ("#a900e3", data[1])

    return ("#ff00ff", "**Error**: %s"%data[1])


def parse_send(user, message):
    sql_command = "SELECT chat_level FROM chat_users WHERE user_id = \"%s\";"%user.id
    crsr.execute(sql_command)
    print(crsr.fetchall())




if __name__ == '__main__':
    start()

    create_users_table()

    close()
