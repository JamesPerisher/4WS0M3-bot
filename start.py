from discord_bot import client, setup, push_live_chat
import minecraft_client
import sys







if __name__ == '__main__':

    c = minecraft_client.minecraft_client(sys.argv[2], sys.argv[3], sys.argv[4], auto_connect=True)
    setup(client, c.send_message)
    c.add_chat_event(push_live_chat)


    client.run(sys.argv[1])
