import sqlite3


class database(sqlite3.Connection):
    def __init__(self, db):
        self.db = db

        self.create_users_table()



    def create_users_table(self):
        global connection, crsr
        sql_command = """CREATE TABLE IF NOT EXISTS chat_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username STRING,
        chat_level INTEGER,
        colour VARCHAR(8),
        renewals INTEGER,
        end_date INTEGER);"""
        self.db.execute(sql_command)

    def add(self, user_id, chat_level, colour, end_date):
        if not self.ifRecord(str(user_id)):
            sql_command = "INSERT INTO chat_users VALUES (NULL, \"%s\", %s, \"%s\", 0, %s);" %(user_id, chat_level, colour, end_date)
            self.db.execute(sql_command)

    def renew(self, user_id, end_date):
        if not self.ifRecord(str(user_id)):
            sql_command = "UPDATE chat_users SET end_date = %s WHERE user_id = \"%s\";" %(end_date, user_id)
            self.db.execute(sql_command)

            sql_command = "UPDATE chat_users SET renewals = renewals + 1 WHERE user_id = \"%s\";"%(user_id)
            self.db.execute(sql_command)

    def new_level(self, user_id, chat_level):
        if not self.ifRecord(str(user_id)):
            sql_command = "UPDATE chat_users SET chat_level = \"%s\" WHERE user_id = \"%s\";"%(chat_level, user_id)
            self.db.execute(sql_command)

    def get_user(self, user_id):
        sql_command = "SELECT * FROM chat_users WHERE user_id = \"%s\";"%user_id
        self.db.execute(sql_command)
        return self.db.fetchall()

    def ifRecord(self, user_id):
        global connection, crsr
        sql_command = "SELECT COUNT(1) FROM chat_users WHERE user_id = \"%s\";"%user_id
        self.db.execute(sql_command)
        if self.db.fetchall()[0][0] == 0:
            return False
        return True

    def get_chat(self, user_id):
        user = self.get_user(user_id)
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


    def change_colour(self, user_id, colour):
        sql_command = "UPDATE chat_users  SET colour = \"%s\" WHERE user_id = \"%s\"" %(colour, user_id)
        self.db.execute(sql_command)

    def change_username(self, user_id, username):
        sql_command = "UPDATE chat_users  SET username = \"%s\" WHERE user_id = \"%s\"" %(username.replace("\\", ""), user_id)
        self.db.execute(sql_command)


    def parse(self, data):
        if data == None or data == "":
            return None
        if data[1].strip() == "":
            return None

        if data[0]:
            return (0xff7700, data[1])

        sp = data[1].split(">")
        user = sp[0].split("<")
        message = ">".join(sp[1::])
        if len(user) == 2:
            if message[1] == ">":
                return (0x076108, "**<%s> **%s" %(user[1], message))
            else:
                if user[1] in ["PaulN07", "PaulN07_1", "StashX"]:
                    return (0x7e0000, "**<%s> **%s" %(user[1], message))
                return (0x1f2999, "**<%s> **%s" %(user[1], message))

        if data[1].split(" ")[1] == "whispers:":
            if not ">" in data[1].split(" ")[0]:
                return (0xa900e3, data[1])
        if " ".join(data[1].split(" ")[1::]) == "joined the game":
            if not ">" in data[1].split(" ")[0]:
                return (0xa900e3, data[1])

        return (0xffffff, "%s"%data[1])


    def parse_send(self, user, message):
        sql_command = "SELECT chat_level FROM chat_users WHERE user_id = \"%s\";"%user.id
        self.db.execute(sql_command)
        print(self.db.fetchall())
