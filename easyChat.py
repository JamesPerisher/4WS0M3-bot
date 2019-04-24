import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import sys


print("Version: %s"%discord.__version__)

Client = discord.Client()
bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Minecraft"))
    print("Bot Online")
    print("Name : %s" %client.user.name)
    print("ID: %s" %client.user.id)
    print("==================================================")


@client.event
async def on_message(message):
    global ch
    if message.author == client.user:
        return
    if message.channel.id == "563532653673054209":
        if message.author.id == "508296387985801226":
            mes = message.embeds[0]['description'][3::]

            mes = mes.split(">** ")

            user = mes[0].strip()
            line = "%s> %s" %(user, ">** ".join(mes[1::]))
            print(user, line)

            embed=discord.Embed(title=line, color=0x004672)
            try:
                if mes[1][0] == ">":
                    embed=discord.Embed(title=line, color=0x009e0a)
            except:
                pass

            if user in ["PaulN07","PaulN07\\_1"]:
                embed=discord.Embed(title=line, color=0x7e0000)

            if user in ["Jkookaburra"]:
                embed=discord.Embed(title=line, color=0x1f8b4c)

            if len(mes) == 1:
                embed=discord.Embed(title=mes[0], color=0xe56706)

            if not line == "":
                await client.send_message(client.get_channel("565114743975575572"), embed=embed)

client.run(sys.argv[1], bot=False)
