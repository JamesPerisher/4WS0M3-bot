from discord_bot import client, setup, push_live_chat
from threading import Thread
import minecraft_client
import sys


class discord_thread(Thread):
    def __init__(self, client, minecrftInstance, botToken):
        super().__init__()

        self.client = client
        self.botToken = self.token = botToken
        self.minecrftInstance = self.mc = minecrftInstance
        setup(self.client, self.mc.send_message)

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








if __name__ == '__main__':
    # argv args : file_path token mc_email mc_pass mc_server

    c = chat_thread(sys.argv[2], sys.argv[3], sys.argv[4], True, push_live_chat)

    d = discord_thread(client, c.mc, sys.argv[1])

    c.start()
    d.start()

    while True:
        inp = input("> ")
        c.mc.send_message(inp)
