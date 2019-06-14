import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import sys
import time

global isqueue
isqueue = False

print(time.time())
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
    global isqueue
    if message.author == client.user:
        return
    if message.channel.id == 563532653673054209:
        if message.author.id == 508296387985801226:
            user = None
            raw_text = message.embeds[0].description
            if raw_text[0][0] != "*": # checks to see if it is a death message
                embed = discord.Embed(title=raw_text, color=0xff7f00)
                try:
                    if raw_text[0:18] == "Position in queue:":
                        print("Queue: %s"%raw_text)
                        if not isqueue:
                            embed = discord.Embed(title="Currently waiting in queue", color=0xff7f00)
                            isqueue = True
                        else:
                            return
                    else:
                        isqueue = False
                except:
                    print("error ignore queue")
            else:
                split_text = raw_text.split(">**")
                #USERNAME

                user = split_text[0]
                user = user.replace("**<", "").replace("\\_", "")

                #text
                #print(unedited_text)
                text = split_text[1][1::]
                if text[0] == " ":
                    text = text[1::]
                elif text[0] == " >":
                    text = text[2::]

                message = ("**<%s>** %s" %(user, text))

                message = message.replace("zozzle.gg", "discord.gg").replace("**", "")


            text=discord.Embed(title=message, color=0x004672)   # at this point 'text' is a message
            try:
                if split_text[1][1] == ">":
                    text=discord.Embed(title=message, color=0x009e0a)
            except:
                pass

            if not user == None:
                if user in ["PaulN07","PaulN07\\_1"]:
                    text=discord.Embed(title=message, color=0x7e0000)

                if user in ["JKookaburra", "JKookaburra_1", "JKookaburra_2", "JKookaburra_3", "JKookaburra_4", "JKookaburra_5", "JKookaburra_6"]:
                    text=discord.Embed(title=message, color=0x1f8b4c)

                user = split_text[0].replace("**<", "")
                #TEXT
                text = ">**".join(split_text[1::])[1::]
                #FULL MESSAGE
                message = ("**%s** %s" %(user, text))

                message = message.replace("zozzle.gg", "discord.gg")

                if text[0] == ">":
                    embed = discord.Embed(title=message, color=0x009e0a)
                else:
                    embed = discord.Embed(title=message, color=0x004672)

                if user in ["PaulN07","PaulN07\\_1"]:
                    embed = discord.Embed(title=message, color=0x7e0000)

                if user in ["JKookaburra", "JKookaburra_1", "JKookaburra_2", "JKookaburra_3", "JKookaburra_4", "JKookaburra_5", "JKookaburra_6"]:
                    embed = discord.Embed(title=message, color=0x1f8b4c)


            if not message == "":
                print(embed.title)
                await client.get_channel(565114743975575572).send(embed=embed)


client.run(sys.argv[1], bot=False)
