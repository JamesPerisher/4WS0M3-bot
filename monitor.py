import discord
from discord.ext.commands import Bot,has_permissions,CheckFailure
from discord.ext import commands
import asyncio
import time
import sys


print(time.time())
print("Version: %s"%discord.__version__)

client = commands.Bot(command_prefix=".")



@client.event
async def on_ready():
    inp = input("1) servers and channels\n2) roles\n3) roles and members\n> ")
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

client.run(sys.argv[1])
