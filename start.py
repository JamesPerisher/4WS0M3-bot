from discord_bot import client, setup, push_live_chat
from threading import Thread
import minecraft_client
import sqlite3
import sys


class discord_thread(Thread):
    def __init__(self, client, minecrftInstance, botToken, db):
        super().__init__()

        self.client = client
        self.botToken = self.token = botToken
        self.db = db
        self.minecrftInstance = self.mc = minecrftInstance
        setup(self.client, self.db, self.mc.send_message)

    def run(self):
        self.client.run(self.token)



class chat_thread(Thread):
    def __init__(self, email, passw, server, reconnect=True, chat_event = lambda x: None):
        super().__init__()

        self.email = email
        self.server = server
        self.reconnect = reconnect

        self.mc = minecraft_client.minecraft_client(self.email, passw, self.server, auto_connect=self.reconnect)
        self.mc.add_chat_event(chat_event)


    def run(self):
        pass


class que_thread(Thread):
    def __init__(self, email, passw, server, time=60):
        super().__init__()

        self.email = email
        self.server = server
        self.time = time

        self.mc = minecraft_client.minecraft_client(self.email, passw, self.server, auto_connect=False)
        self.mc.add_chat_event(lambda x: self.que_callback(x))

    def que_callback(self, x):
        if x == None:
            return False
        try:
            self.user_callback(int(x[1].split(":")[-1].strip()))
        except:
            print("error in: ", end="")
            print(self.que_callback)
        self.mc.disconnect()


    def get_que(self, callback):
        self.user_callback = callback
        self.mc.connect()

    def run(self):
        return


class database_Thread(Thread):
    def __init__(self, location):
        super().__init__()

        self.isready = False
        self.location = location
        self.connection = None
        self.crsr = None

        self.db_start()

    def run(self):
        return

    def db_start(self):
        self.isready = True
        self.connection = sqlite3.connect(self.location, check_same_thread=False)
        print(self.connection)
        self.crsr = self.connection.cursor()

    def commit(self):
        return self.connection.commit()

    def close():
        self.isready = False
        try:
            self.connection.commit()
        except:
            pass
        return self.connection.close()

    def call(self, sql_command):
        self.commit()
        return self.crsr.execute(sql_command)

    def fetchall(self):
        f = self.crsr.fetchall()
        return f

    def execute(self, sql_command):
        return self.call(sql_command)








if __name__ == '__main__':
    # argv args : file_path token mc_email mc_pass mc_server

    def a(x):
        print("my que: ", end="")
        print(x)
        return

    c = chat_thread(sys.argv[2], sys.argv[3], sys.argv[4], True, push_live_chat)
    db = database_Thread("data/database.db")
    d = discord_thread(client, c.mc, sys.argv[1], db)
    # q = que_thread(sys.argv[2], sys.argv[3], "2b2t.org")

    c.start()
    db.start()
    d.start()
    # q.start()

    # q.get_que(a)

    while True:
        inp = input("> ")
        c.mc.send_message(inp)
