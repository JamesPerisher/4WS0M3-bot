import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

import random
import time, pytz
from datetime import datetime,timedelta
import sys
import urllib.request as request
import db_interact


testing = True
print("Version: %s"%discord.__version__)
#Client = discord.Client()
bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)

help = """```
Information:
  help         Shows this message.
  ping         Get a test reponse
  info         Get info on user
  server       Minecrft Server Information
  player       Minecrft Player Information
  about        My creator

Utilities:
  math         do math
  random       generate random numbers
  admin-help   admin commands help

Spam:
  genocide     Whatch the snappening
  Penis        Display Penis
  yodish       Yoda speak Yes, hmmm.

Fun:
  eight-ball   Ask the 8-ball
  fact         Weird facts!
  food         In case you get hungry

Type ?help command for more info on a command.
You can also type ?help category for more info on a category.
```"""

admin_help_text = """```
configuration:
  chat         Set games chat channel
  ascii        Allow ascii art

Type ?help command for more info on a command.
You can also type ?help category for more info on a category.
```"""


#===========================EVENTS===========================


@client.event
async def on_ready():  # bot start event
    if not testing:
        client.loop.create_task(presence_task())
    print("Bot Online")
    print("Name : %s" %client.user.name)
    print("ID: %s" %client.user.id)
    print("==================================================")

@client.event
async def on_message(message):  # on message event
    message.content = message.content.lower().strip()
    try:  # remove this and try to make it work
        #TODO why do we strip again?   >   didnt work without strip
        if message.content.strip()[1::].strip() == "help":
            await message.channel.send(help)
            return
        #TODO why do we strip again? elif?????   >   not elif chance for error not nessasary, didnt work without strip
        if message.content.strip()[1::].split(" ")[1].lower() in ["information","utilities","spam","fun"]:
            await message.channel.send(help)
            return
    except:
        pass

    if message.author.id == client.user.id: # ignore messaged from myself
        return

    if message.channel.id == "565114743975575572": # message.embeds forwarder (takes game chat from another of my discords and forwards it to the new one) (cos u cant have that code)
        db_interact.start()
        for i in db_interact.all_chat():
            await client.send_message(client.get_channel(i), embed=discord.Embed(**message.embeds[0]))

        db_interact.close()

    if message.author.id == "391109829755797514": # admin-my_commands commands - ignore these
        if message.content.startswith("%sNewPresence" %bot_prefix):  # force change of presence
            await new_pres()


    await client.process_commands(message)  # process commands


#===========================TASKS===========================


async def new_pres(): # presence changer
    new_pres = random.choice(["with the constructs of reality", "on the worst server ever", "on 2b2t.org", "kill the nooby"])
    await client.change_presence(activity=discord.Game(name=new_pres))

async def presence_task(): # presence task
    while True:
        await new_pres()
        await asyncio.sleep(random.randint(5, 5*60))  # changes presence every 5seconds to 5mins


#===========================COMMANDS===========================


@client.command(pass_context=True,
                name="ping",
                description="Gets a test reponse from the bot",
                brief="Get a test reponse")
async def ping(ctx):  # ping command
    current_time = time.time()
    send_time = time.mktime(ctx.message.created_at.timetuple()) # sent time
    reponse_time = round((current_time - send_time)/1000, 2) # time between send_time and now

    await ctx.send('Pong! %sms' %reponse_time)



@client.command(pass_context=True,
                name="eight-ball",
                description="Get a answer from the magic 8 ball",
                brief="Ask the 8 ball",
                aliases=["8-ball", "8ball, eight_ball"])
async def eight_ball(ctx):  # eight-ball command
    options = ["Yes", "No", "yes definitely", "it is decidedly so", "signs point to Yes", "it is certain", "without a doubt",
            "most likely", "outlook good", "outlook not so good", "as I see it Yes", "better not tell you now", "cannot predict now",
            "MY REPLY IS NO", "you may rely on it", "REPLY hazy try again", "ask again later", "concentrate and ask again",
            "don't count on it", "very doubtful", "my sources say no"]  # all options

    await ctx.send("The magic 8-ball says %s" %random.choice(options).upper())


@client.command(pass_context=True, name="server",
                description="Gets status of a Minecraft server", brief="Minecrft Server Information",
                aliases=["server-info", "info-server"])
async def server_info(ctx, server=None):  # server-info command
        if server == None:
            await ctx.send("```Gets status of a Minecraft server\n\n?[server|server-info|info-server] <server>```")
            return
        r = request.urlopen('https://mcapi.us/server/status?ip=%s' %server)
        a = eval(r.read().decode().replace(":false,", ":False,").replace(":true,", ":True,"))

        if a["status"] == "error":
            await ctx.send("```error resolving server %s```" %server)
            return

        if a["last_online"] == "":
            lonlone = "Has never been online"
        else:
            str(datetime.fromtimestamp(int(a["last_online"])).astimezone(pytz.utc)).split("+")[0]

        if not a["online"]:
            embed=discord.Embed()
            embed.set_author(name="%s" %server, icon_url="https://cdn.discordapp.com/attachments/555690428964536333/568621320061845505/580b57fcd9996e24bc43c2f1.png")
            embed.add_field(name="online", value=a["online"], inline=True)
            embed.add_field(name="last online", value=lonlone, inline=True)
            embed.add_field(name="last checked", value=str(datetime.fromtimestamp(int(a["last_updated"])).astimezone(pytz.utc)).split("+")[0], inline=True)
            await ctx.send(embed=embed)
            return

        for i in ['§4', '§c', '§6', '§e', '§2', '§a', '§b', '§3', '§1', '§9', '§d', '§5', '§f', '§7', '§8', '§0', '§l', '§m', '§n', '§o', '§r']:
            a["motd"] = a["motd"].replace(i, "")


        embed=discord.Embed(description=a["motd"], color=0x7e0000)
        embed.set_author(name="%s" %server, icon_url="https://eu.mc-api.net/v3/server/favicon/%s" %server)
        embed.add_field(name="online", value=a["online"], inline=True)
        embed.add_field(name="max players", value=a["players"]["max"], inline=True)
        embed.add_field(name="current players", value=a["players"]["now"], inline=True)
        embed.add_field(name="versions", value=a["server"]["name"], inline=True)
        embed.add_field(name="last online", value=str(datetime.fromtimestamp(int(a["last_online"])).astimezone(pytz.utc)).split("+")[0], inline=True)
        embed.add_field(name="last checked", value=str(datetime.fromtimestamp(int(a["last_updated"])).astimezone(pytz.utc)).split("+")[0], inline=True)
        await ctx.send(embed=embed)


async def info(ctx, user):
    m = ctx.messagectx.guild.get_member(user.id)  # get member object (da fuck i need this and not a user object idk)

    embed=discord.Embed(color=m.colour)  # embed (colour has a u cos aussie)
    embed.set_author(name="%s#%s" %(user.name,user.discriminator), icon_url=user.avatar_url)
    embed.add_field(name="ID:", value=user.id, inline=True)
    embed.add_field(name="Status:", value=m.status, inline=True)
    if not m.game == None:
        embed.add_field(name="presence:", value="Playing %s" %m.game, inline=True)
    else:
        embed.add_field(name="presence:", value="None", inline=True)

    embed.add_field(name="Bot:", value=str(user.bot), inline=True)
    embed.add_field(name="Colour:", value=str(m.colour), inline=True)
    embed.add_field(name="Account creation (UTC):", value=str(user.created_at).split(".")[0], inline=True)

    await ctx.send(embed=embed)  # say embed



@client.command(pass_context=True, name="info",
                description="Get info on a user via mention or id", brief="Get info on user",
                aliases=["get-info"])
async def get_info(ctx, user=None):  # info command
    try:
        if user == None: # no user passed
            user = ctx.message.author.id

        if user[0:2] == "<@" and user[-1] == ">":  # mention to id
            user = user[2:-1]

        u = await client.get_user(user)
        await info(ctx, u)
        return
    except Exception as e:
        await ctx.send("You fucked up: %s" %e)  # catch errors


@client.command(pass_context=True, name="math",
                description="calculate maths stuff (you can use pi as π)", brief="do math",
                aliases=["calc", "cal"])
async def math(ctx, *args):  # math command
    raw_equation = " ".join(args)
    equation = raw_equation.replace(" ", "").replace("^", "**").replace("e", "*10**").replace("pi", "3.14159265358979323846").replace("π", "3.14159265358979323846")
    equation = list(equation)
    for i in range(len(equation)):
        letter = equation[i]
        if letter not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '/', '*', '%', '.', '(', ')']:
            equation[i] = "$"
    equation = "".join(equation).replace("$", "")
    out = eval(equation)
    await ctx.send("%s ≈ %s" %(raw_equation, out))


@client.command(pass_context=True, name="genocide",
                description="The great feared snappening", brief="Whatch the snappening",
                aliases=["snappening", "snap"])
async def genocide(ctx):  # genocide command
    e = discord.Embed(title="You should have gone for the head")
    e.set_image(url="https://cdn.discordapp.com/attachments/510365719217831936/565456017710907393/MilkyBriskAnura-size_restricted.gif")
    await ctx.send(embed=e)

@client.command(pass_context=True, name="random",
                description="Generate a number between to numbers", brief="Random number",
                aliases=["rand"])
async def randomint(ctx, min=None, max=None):  # random-int command
    if min == None:
        min=0
    if max == None:
        max=100
    try:
        await ctx.send(str(random.randint(int(min), int(max))))
    except Exception as e:
        await ctx.send("You fucked up: %s" %e)  # catch errors


@client.command(pass_context=True, name="fact",
                description="Sends a random fun fact", brief="Weird facts!",
                aliases=["facts"])
async def randomfact(ctx):  # fact command
    with open("facts.txt", "r") as f:
        lines = f.readlines()
        await ctx.send(random.choice(lines))

@client.command(pass_context=True, name="food",
                description="Sends a random food item", brief="In case you get hungry",
                aliases=["foods"])
async def getfood(ctx):  # foods command
    db_interact.start()
    if db_interact.is_ascii(ctx.messagectx.guild):
        with open("ascii_art.txt", "r") as f:
            lines = f.readlines()
            await ctx.send("```%s```" %random.choice(lines).replace("\\n", "\n"))
    else:
        await ctx.send("```Ascii art is disabled on this server idk why tho.```")
    db_interact.close()

@client.command(pass_context=True, name="penis",
                description="Get your penis size", brief="Display Penis")
async def penis(ctx):  # penis command
    if ctx.message.author.id == "391109829755797514":
        await ctx.send("8%sD" %("="*10))
    else:
        await ctx.send("8%sD" %("="*random.randint(1, 9)))


@client.command(pass_context=True, name="yoda",
                description="Converts normal English into yodish", brief="Yoda speak Yes, hmmm.",
                aliases=["yodish"])
async def yoda(ctx):  # yoda command
    s = " ".join(ctx.message.content.split(" ")[1::])

    out = []
    for i in s.split("."):
        if i == "":
            continue
        x = i.strip().split(" ")

        out = out + x[2::]+x[0:2]+["."]
    await ctx.send(" ".join(out + [random.choice(["--point1003t5--Yes, hmmm.", "--point1003t5--Hmmmmmm", "--point1003t5--Yeesssssss.", "--point1003t5--Herh herh herh.", "--point1003t5--."])]).replace(". --point1003t5--", " ").replace(" .", "."))



@client.command(pass_context=True, name="admin-help",
                description="Get help on admin command", brief="admin commands help",
                aliases=["help-admin", "admin"])
async def admin_help(ctx):  # admin-help command
    await ctx.send(admin_help_text)

@client.command(pass_context=True, name="chat",
                description="Set the channel for the in-game chat from channel name or id", brief="Set games chat channel")
async def chat(ctx, channel):  # chat command
    if not ctx.channel.permissions_for(ctx.author).administrator:
        await ctx.send("```You do not have permission to do that!```")
        return
    try:
        channel = client.get_channel(str(channel).replace("<", "").replace(">", "").replace("#", ""))
    except Exception as e:
        print(e)
    else:
        if str(channel).strip().lower() == "0" or str(channel).strip().lower() == "none":
                channel = lambda : print(end="")
                channel.id = 0
                channel.name = "None"
        db_interact.start()
        db_interact.update_channel(ctx.messagectx.guild, channel.id)
        db_interact.close()
        await ctx.send("```Set in-game live chat to: %s```" %channel.name)

@client.command(pass_context=True, name="ascii",
                description="Configure ascii art allowence with [True/False]", brief="Allow ascii art")
async def ascii(ctx, config):  # ascii command
    if not ctx.message.author.server_permissions.administrator:
        await ctx.send("```You do not have permission to do that!```")
        return
    db_interact.start()
    if config.lower().strip() == "true":
        await ctx.send("```Updated show ascii to True```")
        db_interact.update_ascii(ctx.messagectx.guild, 1)
    if config.lower().strip() == "false":
        await ctx.send("```Updated show ascii to False```")
        db_interact.update_ascii(ctx.messagectx.guild, 0)
    db_interact.close()


@client.command(pass_context=True, name="about",
                description="Get details of my creator", brief="My creator")
async def about(ctx):  # about command
    embed=discord.Embed(color=0x7e0000)
    embed.set_author(name="%s#%s (BOT)" %(client.user.name,client.user.discriminator), icon_url=client.user.avatar_url)
    embed.add_field(name="Created by:", value="%s#%s" %((client.get_user(391109829755797514).name), (client.get_user(391109829755797514)).discriminator), inline=False)
    embed.add_field(name="Created in:", value="Python 3.6.x with discord API", inline=False)
    embed.add_field(name="Runs in:", value="Python 3.7.x updated by JKookaburra", inline=False)
    embed.add_field(name="Hosted by:", value="%s#%s" %((client.get_user(391340428315852801)).name, (client.get_user(391340428315852801)).discriminator), inline=False)
    embed.set_footer(text="PM PaulN07 (@%s#%s) for info/inquiries/bug reports" %((client.get_user(391109829755797514)).name, (client.get_user(391109829755797514)).discriminator))
    await ctx.send(embed=embed)




@client.command(pass_context=True, name="player",
                description="Gets info on Minecraft player", brief="Minecrft Player Information",
                aliases=["player-info", "info-player"])
async def player_info(ctx, username=None):  # player-info command
    username = username.replace("\\_", "_")
    if username == None:
        await ctx.send("``Gets info on Minecraft Player\n\n?[player|player-info|info-player] [username]```")
        return
    try:
        r = request.urlopen('https://api.mojang.com/users/profiles/minecraft/%s' %username)
        a = eval(r.read().decode().replace(":false,", ":False,").replace(":true,", ":True,"))
        r = request.urlopen('https://api.mojang.com/user/profiles/%s/names' %a["id"])
        b = eval(r.read().decode().replace(":false,", ":False,").replace(":true,", ":True,"))
        request.urlopen("https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
        request.urlopen("https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
        names = ""
        for i in b:
            names = names + ", " + str(i["name"])
        names = names[1::]


        embed=discord.Embed(color=0x7e0000)
        embed.set_author(name=a["name"], icon_url="https://crafatar.com/avatars/%s" %a["id"])
        embed.set_thumbnail(url="https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
        embed.add_field(name="uuid", value=a["id"], inline=True)
        embed.add_field(name="name history", value=names, inline=True)
        embed.add_field(name="Name MC", value="https://namemc.com/profile/%s"%a["id"], inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send("```No current player named: %s```" %username)




client.run(sys.argv[1])  # start client
