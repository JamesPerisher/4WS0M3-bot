import discord
from discord.ext.commands import Bot,has_permissions,CheckFailure
from discord.ext import commands
import asyncio
import time
import sys
import base64


print(time.time())
print("Version: %s"%discord.__version__)

client = commands.Bot(command_prefix=".")



@client.event
async def on_ready():
    while True:
        inp = input("1) servers and channels\n2) roles\n3) roles and members\n4) ids and names\n> ")
        if inp == "1":
            print("\nServers")
            for i in client.guilds:
                print("+---%s"%i.name)
                for j in i.categories:
                    print("|   +---%s"%j.name)
                    for k in j.text_channels:
                        print("|   |       %s"%k.name)
                    for k in j.voice_channels:
                        print("|   |       %s"%k.name)
                print("|\n|")
        if inp == "2":
            print("\nServers")
            for i in client.guilds:
                print("+---%s"%i.name)
                for j in i.roles:
                    print("|   +---%s"%j.name)

        if inp == "3":
            print("\nServers")
            for i in client.guilds:
                print("+---%s"%i.name)
                for j in i.roles:
                    print("|   +---%s"%j.name)
                    for k in j.members:
                        print("|   |       %s"%str(k))
        if inp == "4":
            out = {}
            print("\nServers")
            for i in client.guilds:
                print("+---%s"%i.name)
                for j in i.roles:
                    for k in j.members:
                        out[k.id] = str(k)
            print("\n".join(["%s: %s" %(x, out[x]) for x in out]))

        if inp == "5":
            out = base64.b85decode(input("token >").replace(".","*").replace(" ","").encode()).decode().split("-")
            print(client.get_user(int(out[1])))
            print(out)

client.run(sys.argv[1])
