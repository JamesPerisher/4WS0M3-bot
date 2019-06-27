import sqlite3
import json


with open("data/coins.json", "r") as f:
    coin_info  = json.load(f)
    f.close()
def data_track():
    with open("data/coins.json", "w") as f:
        f.truncate()
        json.dump(coin_info, f)

def start():
    global connection, crsr
    connection = sqlite3.connect("data/coins.db")
    crsr = connection.cursor()

def create_servers_table():
    global connection, crsr
    sql_command = """
    CREATE TABLE IF NOT EXISTS balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(20),
    amount DESCIMAL);"""
    crsr.execute(sql_command)

def ifRecord(user_id):
    global connection, crsr
    sql_command = "SELECT COUNT(1)\n    FROM balances\n    WHERE user_id = \"%s\";"%user_id
    crsr.execute(sql_command)
    if crsr.fetchall()[0][0] == 0:
        return False
    else:
        return True

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




def balance(user_id):
    if ifRecord(user_id):
        sql_command = "SELECT amount FROM balances WHERE user_id = %s" %user_id
        crsr.execute(sql_command)
        return crsr.fetchall()[0][0]
    else:
        sql_command = "INSERT INTO balances VALUES (NULL, %s, 0)" %user_id
        crsr.execute(sql_command)
        print("Added %s to coins db" %user_id)
        return 0

def add(user_id, amt):
    sql_command = "UPDATE balances SET amount = %s WHERE user_id = %s" %(balance(user_id)+amt, user_id)
    crsr.execute(sql_command)
    return True

def buy(user_id, amt):
    if add(user_id, amt):
        coin_info["coins"]["total"] += amt
        coin_info["coins"]["paid"] += amt
        data_track()

def create(user_id, amt):
    if add(user_id, amt):
        coin_info["coins"]["total"] += amt
        coin_info["coins"]["created"] += amt
        data_track()

def send(from_user, to_user, amt):
    if amt > 0:
        if (balance(from_user) - amt) >= 0:
            add(from_user, -amt)
            add(to_user, amt)
            return (True, "Successfull")
        else:
            return (False, "Insufficient funds")
    else:
        return (False, "Can not send negative amount")

def top(users):
    sql_command = "SELECT * FROM balances ORDER BY amount DESC LIMIT %s;"%users
    crsr.execute(sql_command)
    return crsr.fetchall()


if __name__ == '__main__':
    start()
    create_servers_table() # makes the empty database
    close()
