import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import sys

print("Version: %s"%discord.__version__)
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
    if message.author == client.user:
        return
    if message.channel.id == 563532653673054209:
        if message.author.id == 508296387985801226:
            raw_text = message.embeds[0].description
            #print(raw_text)

            if raw_text[0][0] != "*": # checks to see if it is a death message
                embed = discord.Embed(title=raw_text, color=bc0000)
            else:
                split_text = raw_text.split(">**")
                #USERNAME
                user = split_text[0].replace("**<", "")
                #TEXT
                text = ">**".join(split_text[1::])[1::]
                #FULL MESSAGE
                message = ("**%s** %s" %(user, text))

                message = message.replace("zozzle.gg", "discord.gg")
                print(message)
                if text[0] == ">":
                    embed = discord.Embed(title=message, color=0x009e0a)
                else:
                    embed = discord.Embed(title=message, color=0x004672)

                if user in ["PaulN07","PaulN07\\_1"]:
                    embed = discord.Embed(title=message, color=0x7e0000)

                if user in ["JKookaburra", "JKookaburra_1", "JKookaburra_2", "JKookaburra_3", "JKookaburra_4", "JKookaburra_5", "JKookaburra_6"]:
                    embed = discord.Embed(title=message, color=0x1f8b4c)


            if not message == "":
                await client.get_channel(565114743975575572).send(embed=embed)

client.run(sys.argv[1], bot=False)
