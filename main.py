import discord
from discord.ext.commands import Bot,has_permissions,CheckFailure
from discord.ext import commands
import asyncio

import random
import time, pytz
from datetime import datetime,timedelta
import sys
import urllib.request as request
import json
from math import *
import base64

import db_interact
import mc_queue
import coins

global last, run
last = None
run = False

configuration = json.load(open("data/config.json"))

mc_queue.que_update = configuration["queue"]["que_update"]
testing = True   # database, database intereaction and more will not work faster for me testing
print(time.time())
print("Version: %s"%discord.__version__)
bot_prefix = configuration["bot"]["prefix"]
colour = configuration["bot"]["bot_colour"]

# TODO: https://repl.it/talk/learn/Discordpy-Rewrite-Tutorial-using-commands-extension/10690

client = commands.Bot(
    command_prefix=bot_prefix,
    description="PaulN07's bot",
    owner_id=391109829755797514,
    case_insensitive=True
)


#===========================EVENTS===========================


@client.event
async def on_ready():  # bot start event
    global run
    if not run:
        if not testing:
            client.loop.create_task(presence_task())
            client.loop.create_task(queue_task())
        print("Bot Online")
        print("Name : %s" %client.user.name)
        print("ID: %s" %client.user.id)
        print("==================================================")
        run = True

@client.event
async def on_message(message):  # on message event
    global last
    if message.author.id == client.user.id: # ignore messaged from myself
        return

    if int(message.channel.id) == int(configuration["bot"]["forward_from"]): # message.embeds forwarder (takes game chat from another of my discords and forwards it to the new one) (cos u cant have that code)
        if not testing:
            db_interact.start()
            try:
                for i in db_interact.all_chat():
                    await client.get_channel(int(i)).send(embed=message.embeds[0])
            except:
                pass
            db_interact.close()

    message.content = str(message.content)+str(" ")
    if message.content[0] != configuration["bot"]["prefix"]:
        return

    if message.author.id == configuration["bot"]["owner"]: # admin-my_commands commands - ignore these
        if message.content.startswith("%sNewPresence" %bot_prefix):  # force change of presence
            await new_pres()
            return

    last = message

    await client.process_commands(message)  # process commands


#===========================TASKS===========================


async def new_pres(): # presence changer
    new_pres = random.choice(["with the constructs of reality", "on the worst server ever", "on 2b2t.org", "kill the nooby"])
    await client.change_presence(activity=discord.Game(name=new_pres))

async def presence_task(): # presence task
    while True:
        await new_pres()
        await asyncio.sleep(random.randint(5, 5*60))  # changes presence every 5seconds to 5mins


async def push_que(): # push current que to file
    try:
        mc_queue.start()
        mc_queue.add(*mc_queue.get_queue())
        mc_queue.que24()
        mc_queue.close()
        print("Pushed to mc_queue")
    except:
        print("Add to que failed")

async def queue_task(): # presence task
    while True:
        await push_que()
        await asyncio.sleep(configuration["queue"]["que_update"])

#===========================COMMANDS===========================


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True,
                    name="ping",
                    description="Gets a test response from the bot",
                    brief="Get a test response")
    async def ping(self, ctx):  # ping command
        current_time = time.time()
        send_time = time.mktime(ctx.message.created_at.timetuple()) # sent time
        reponse_time = round((current_time - send_time)*100, 2) # time between send_time and now
        await ctx.send('Pong! %sms' %reponse_time)



    @commands.command(pass_context=True, name="info",
                    description="Get info on a user via mention or id", brief="Get info on user",
                    aliases=["get-info"])
    async def get_info(self, ctx, user=None):  # info command
        try:
            if user == None: # no user passed
                user = ctx.message.author.id

            if user[0:2] == "<@" and user[-1] == ">":  # mention to id
                user = user[2:-1]

            u = client.get_user(int(user))
            m = ctx.guild.get_member(u.id)  # get member object (da fuck i need this and not a user object idk)

            embed=discord.Embed(color=m.colour)  # embed (colour has a u cos aussie)
            embed.set_author(name="%s#%s" %(u.name,u.discriminator), icon_url=u.avatar_url)
            embed.add_field(name="ID:", value=u.id, inline=True)
            embed.add_field(name="Status:", value=m.status, inline=True)
            if not m.activity  == None:
                embed.add_field(name="presence:", value="Playing %s" %m.activity , inline=True)
            else:
                embed.add_field(name="presence:", value="None", inline=True)

            embed.add_field(name="Bot:", value=str(u.bot), inline=True)
            embed.add_field(name="Colour:", value=str(m.colour), inline=True)
            embed.add_field(name="Account creation (UTC):", value=str(u.created_at).split(".")[0], inline=True)

            await ctx.send(embed=embed)  # say embed
            return
        except Exception as e:
            await ctx.send("Invalid user")  # catch errors



    @commands.command(pass_context=True, name="server",
                    description="Gets status of a Minecraft server", brief="Minecrft Server Information",
                    aliases=["server-info", "info-server"])
    async def server_info(self, ctx, server=None):  # server-info command
            if server == None:
                await ctx.send("```Gets status of a Minecraft server\n\n?[server|server-info|info-server] <server>```")
                return
            r = request.urlopen('https://mcapi.us/server/status?ip=%s' %server)
            a = json.loads(r.read().decode())

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


            embed=discord.Embed(description=a["motd"], color=eval("0x%s"%colour))
            embed.set_author(name="%s" %server, icon_url="https://eu.mc-api.net/v3/server/favicon/%s" %server)
            embed.add_field(name="online", value=a["online"], inline=True)
            embed.add_field(name="max players", value=a["players"]["max"], inline=True)
            embed.add_field(name="current players", value=a["players"]["now"], inline=True)
            embed.add_field(name="versions", value=a["server"]["name"], inline=True)
            embed.add_field(name="last online", value=str(datetime.fromtimestamp(int(a["last_online"])).astimezone(pytz.utc)).split("+")[0], inline=True)
            embed.add_field(name="last checked", value=str(datetime.fromtimestamp(int(a["last_updated"])).astimezone(pytz.utc)).split("+")[0], inline=True)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, name="player",
                    description="Gets info on Minecraft player", brief="Minecrft Player Information",
                    aliases=["player-info", "info-player"])
    async def player_info(self, ctx, username=None):  # player-info command
        username = username.replace("\\_", "_")
        if username == None:
            await ctx.send("``Gets info on Minecraft Player\n\n?[player|player-info|info-player] [username]```")
            return
        try:
            r = request.urlopen('https://api.mojang.com/users/profiles/minecraft/%s' %username)
            a = json.loads(r.read().decode())
            r = request.urlopen('https://api.mojang.com/user/profiles/%s/names' %a["id"])
            b = json.loads(r.read().decode())
            request.urlopen("https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
            request.urlopen("https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
            names = ""
            for i in b:
                names = names + ", " + str(i["name"])
            names = names[1::]


            embed=discord.Embed(color=eval("0x%s"%colour))
            embed.set_author(name=a["name"], icon_url="https://crafatar.com/avatars/%s" %a["id"])
            embed.set_thumbnail(url="https://crafatar.com/renders/body/%s?size=4&default=MHF_Steve&overlay"%a["id"])
            embed.add_field(name="uuid", value=a["id"], inline=True)
            embed.add_field(name="name history", value=names, inline=True)
            embed.add_field(name="Name MC", value="https://namemc.com/profile/%s"%a["id"], inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("```No current player named: %s```" %username)


    @commands.command(pass_context=True, name="about",
                    description="Get details of my creator", brief="My creator")
    async def about(self, ctx):  # about command
        embed=discord.Embed(color=eval("0x%s"%colour))
        embed.set_author(name="%s#%s (BOT)" %(client.user.name,client.user.discriminator), icon_url=client.user.avatar_url)
        embed.add_field(name="Created by:", value="%s#%s" %((client.get_user(configuration["bot"]["owner"]).name), (client.get_user(configuration["bot"]["owner"])).discriminator), inline=False)
        embed.add_field(name="Created in:", value=configuration["credits"]["created_in"], inline=False)
        embed.add_field(name="Runs in:", value=configuration["credits"]["runs_in"], inline=False)
        embed.add_field(name="Hosted by:", value=configuration["credits"]["host"], inline=False)

        footer_data = configuration["credits"]["footer"]
        for i in range(len(footer_data["users"])):
            footer_data["text"] = footer_data["text"].replace("<name%s>"%i, client.get_user(footer_data["users"][i]).name)
            footer_data["text"] = footer_data["text"].replace("<id%s>"%i, client.get_user(footer_data["users"][i]).discriminator)
        embed.set_footer(text=footer_data['text'])
        await ctx.send(embed=embed)


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, name="math",
                    description="calculate maths stuff (can use sin, pi, sqrt, ect)", brief="do math",
                    aliases=["calc", "cal"])
    async def math(self, ctx, *args):  # math command
        raw_equation = " ".join(args)

        safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log','log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'abs'] # all safe functions
        safe_dict = dict([ (k, locals().get(k, eval(k))) for k in safe_list ])

        # safe_dict['abs'] = abs  # manualy add another item/value
        safe_dict['π'] = pi

        try:
            out = eval(raw_equation,{"__builtins__":None},safe_dict)
        except Exception as e:
            await ctx.send("Invalid equation")
        else:
            await ctx.send("`%s` = `%s`" %(raw_equation, out))



    @commands.command(pass_context=True, name="random",
                    description="Generate a number between to numbers", brief="Random number",
                    aliases=["rand"])
    async def randomint(self, ctx, min="0", max="100"):  # random-int command
        try:
            min = int(min)
            max = int(max)
        except:
            await ctx.send("Numbers entered must be integeres(whole numbers)")
            return
        if max < min:
            a = max
            max = min
            min = a
            del a
        try:
            await ctx.send(str(random.randint(int(min), int(max))))
        except Exception as e:
            await ctx.send("You found a bug! (maybe)")  # catch errors

    @commands.command(pass_context=True,
                    name="que",
                    description="Get queue from 2b2t.org",
                    brief="server queue")
    async def que(self, ctx):  # ping command
        mc_queue.start()
        q = mc_queue.get_last()
        mc_queue.close()
        if isinstance(q[0][1], str):
            await ctx.send("Either 2b2t is down or there was an issue with my bot reason: %s"%q[0][1])
            return
        embed=discord.Embed(color=eval("0x%s"%colour))
        embed.add_field(name="Queue", value=q[0][1], inline=True)
        embed.add_field(name="Priority queue", value=q[0][2] - (q[0][1] + 200), inline=True)
        embed.add_field(name="Online", value=q[0][2], inline=True)
        embed.set_footer(text="NOTE: try the queue command")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True,
                    name="queue",
                    description="Graphs queue from 2b2t.org over time",
                    brief="server queue graph")
    async def queue(self, ctx):  # ping command
        await ctx.send(file=discord.File("data/que-graphs/current.png", filename="data/que-graphs/current.png", spoiler=False))

    @commands.command(pass_context=True, name="admin-help",
                    description="Get help on admin command", brief="admin commands help",
                    aliases=["help-admin", "adminhelp","admin"])
    async def admin_help(self, ctx):  # admin-help command
        await ctx.send(admin_help_text)


class Spam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="genocide",
                    description="The great feared snappening", brief="Whatch the snappening",
                    aliases=["snappening", "snap"])
    async def genocide(self, ctx):  # genocide command
        e = discord.Embed(title="You should have gone for the head")
        e.set_image(url="https://cdn.discordapp.com/attachments/510365719217831936/565456017710907393/MilkyBriskAnura-size_restricted.gif")
        await ctx.send(embed=e)


    @commands.command(pass_context=True, name="penis",
                    description="Get your penis size", brief="Display Penis")
    async def penis(self, ctx):  # penis command
        if ctx.message.author.id == 391109829755797514:
            await ctx.send("8%sD" %("="*10))
        else:
            await ctx.send("8%sD" %("="*random.randint(1, 9)))


    @commands.command(pass_context=True, name="yoda",
                    description="Converts normal English into yodish", brief="Yoda speak Yes, hmmm.",
                    aliases=["yodish"])
    async def yoda(self, ctx):  # yoda command
        s = " ".join(self, ctx.message.content.split(" ")[1::])

        out = []
        for i in s.split("."):
            if i == "":
                continue
            x = i.strip().split(" ")

            out = out + x[2::]+x[0:2]+["."]
        await ctx.send(" ".join(out + [random.choice(["--point1003t5--Yes, hmmm.", "--point1003t5--Hmmmmmm", "--point1003t5--Yeesssssss.", "--point1003t5--Herh herh herh.", "--point1003t5--."])]).replace(". --point1003t5--", " ").replace(" .", "."))


class Coins(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="balance",
                    description="Gets a users balance if none specified gets yours", brief="Your balance",
                    aliases=["bal"])
    async def bal(self, ctx, user=None):  # get player balance bal
        if user == None:
            coins.start()
            user = ctx.message.author
            await ctx.send("<@%s> has a balance of: %s" %(user.id, coins.balance(user.id)))
            coins.close()
            return
        try:
            coins.start()
            user = client.get_user(int(user.replace("<@", "").replace(">", "")))
            await ctx.send("<@%s> has a balance of: %s" %(user.id, coins.balance(user.id)))
            coins.close()
            return
        except ValueError:
            await ctx.send("Invalid user")
            return

    @commands.command(pass_context=True, name="send",
                    description="Transfers coins to another user", brief="Send coins")
    async def send(self, ctx, to_user=None, amt=None):  # transfer coins command send
        if to_user == None or amt == None:
            await ctx.send("usage %ssend [recipient] [amount]"%bot_prefix)
            return
        try:
            coins.start()
            user = client.get_user(int(to_user.replace("<@", "").replace(">", "")))
            send = coins.send(self, ctx.message.author.id,user.id, int(amt))
            if send[0]:
                await ctx.send("Transfer of %s coins was successfull"%amt)
            else:
                await ctx.send(send[1])
            coins.close()
            return
        except ValueError:
            await ctx.send("Invalid value **note:** you can only send full coins")
            return


    @commands.command(pass_context=True, name="create",
                    description="creates coins for user", brief="create coins")
    async def create(self, ctx, user=None, amt=None):  # transfer coins command send
        if ctx.message.author.id in [391109829755797514, 473745930605166593, 540139891904741386]:
            if user == None or amt == None:
                await ctx.send("usage %screate [user] [amount]"%bot_prefix)
                return
            try:
                coins.start()
                user = client.get_user(int(user.replace("<@", "").replace(">", "")))
                coins.create(user.id, int(amt))
                await ctx.send("Creation of %s coins was successfull"%amt)
                coins.close()
                return
            except ValueError:
                await ctx.send("Invalid value **note:** you can only send full coins")
                return
        else:
            await ctx.send("You dont have permission to do that!")

    @commands.command(pass_context=True, name="conf_coin")
    async def conf_coin(self, ctx, user=None, amt=None):  # transfer coins command send
        if ctx.message.author.id in [391109829755797514]:
            if user == None or amt == None:
                await ctx.send("usage %screate [user] [amount]"%bot_prefix)
                return
            try:
                coins.start()
                user = client.get_user(int(user.replace("<@", "").replace(">", "")))
                coins.buy(user.id, int(amt))
                await ctx.send("Creation of %s coins was successfull"%amt)
                coins.close()
                return
            except ValueError:
                await ctx.send("Invalid value **note:** you can only send full coins")
                return
        else:
            await ctx.send("You dont have permission to do that!")

    @commands.command(pass_context=True, name="baltop",
                    description="Get a list of the richest people", brief="The richest peeps")
    async def baltop(self, ctx, user=None, amt=None):  # transfer coins command send
        coins.start()
        out = ["The richest people:"]
        top_users = []
        max_username = 0

        for i in coins.top(20):
            try:
                username = str(client.get_user(int(i[1])))
            except:
                pass
            else:
                max_username = max([len(username), max_username])
                top_users.append((username, i[2]))

        for i in top_users:
            out.append("%s%s%s"%(i[0], " "*(max_username-len(i[0])+2), i[1]))
        await ctx.send("```\n%s```" %"\n".join(out))
        coins.close()

    @commands.command(pass_context=True, name="buy",
                    description="Buy coins through paypal", brief="Buy coins")
    async def buy(self, ctx, amt="50000"):  # buy coins command buy
        # amt default set to about 5 USD
        try:
            amt = int(amt)
        except:
            await ctx.send("```Invalid value: %s```"%amt)
            return

        irl_val = ceil((float(amt)/10000.0)*100)/100
        if irl_val < 1:
            await ctx.send("```Your purchase must be over $1 current val: $%s```"%irl_val)
            return

        try:
            ref_id = str(base64.b85encode(str.encode("1-%s-%s-%s"%(self, ctx.message.author.id, ctx.message.guild.id, round(time.time())))))[2:-1]
            referal = ctx.message.guild.name
        except:
            ref_id = str(base64.b85encode(str.encode("0-%s-%s-%s"%(self, ctx.message.author.id, '000000000000000000', round(time.time())))))[2:-1]
            referal = "Not found"

        embed=discord.Embed(color=0x7e0000)
        embed.set_author(name="Purchase coins")
        embed.add_field(name="coins", value="%s"%amt, inline=False)
        embed.add_field(name="price", value="$%s"%irl_val, inline=False)
        embed.add_field(name="purchase id", value=ref_id, inline=False)
        embed.add_field(name="server referal", value=referal, inline=False)
        embed.set_footer(text="Confirm with %sconfirm or %sclose to cancel"%(bot_prefix, bot_prefix))
        m = await ctx.message.author.send(embed=embed)
        await m.pin()


    def is_ticket(channel):
        if str(type(channel)).split("'")[1] == "discord.channel.DMChannel":
            return "DM"
        return ctx.message.channel.name[0:9] == "ticket-07"


    @commands.command(pass_context=True, name="close",
                    description="Close purchase ticket", brief="Close ticket")
    async def close(self, ctx):  # close ticket command close
        if is_ticket(self, ctx.message.channel) == "DM":
            await ctx.send("ticket closed")
        else:
            if is_ticket(self, ctx.message.channel):
                await ctx.message.channel.delete(reason="ticket closed")
                return

            await ctx.send("```Go to a open ticket and send %sclose to close it```"%bot_prefix)

    @commands.command(pass_context=True, name="confirm",
                    description="Confirm purchase", brief="Confirm purchase")
    async def Confirm(self, ctx):  # confirm purchase command confirm
        if is_ticket(self, ctx.message.channel) or is_ticket(self, ctx.message.channel) == "DM":
            message = "error"
            for i in await ctx.message.channel.pins():
                await i.unpin()
                if i.author.id == client.user.id:
                    message = i
                    break
            if message == "error":
                await ctx.send("There was a ticketing issue")
                return

            em = message.embeds[0].to_dict()
            coins = em['fields'][0]['value']
            val = em['fields'][1]['value']
            id = em['fields'][2]['value']

            await ctx.send("To complete the process, go to https://www.paypal.me/pauln07 and pay the specified amount remember to include the transaction id provided above and/or your discord name preferably id for faster confirmation. **Note: ** Payments are manually authorised and will usually be completed within 24-hour.")

        else:
            await ctx.send("```Go to a open ticket and send %sconfirm to confirm it```"%bot_prefix)




class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True,
                    name="eight-ball",
                    description="Get a answer from the magic 8 ball",
                    brief="Ask the 8 ball",
                    aliases=["8ball", "8-ball", "eight_ball"])
    async def eight_ball(self, ctx):  # eight-ball command
        options = ["Yes", "No", "yes definitely", "it is decidedly so", "signs point to Yes", "it is certain", "without a doubt",
                "most likely", "outlook good", "outlook not so good", "as I see it Yes", "better not tell you now", "cannot predict now",
                "MY REPLY IS NO", "you may rely on it", "REPLY hazy try again", "ask again later", "concentrate and ask again",
                "don't count on it", "very doubtful", "my sources say no"]  # all options

        await ctx.send("The magic 8-ball says %s" %random.choice(options).lower())

    @commands.command(pass_context=True, name="fact",
                    description="Sends a random fun fact", brief="Weird facts!",
                    aliases=["facts"])
    async def randomfact(self, ctx):  # fact command
        with open("data/facts.txt", "r") as f:
            lines = f.readlines()
            await ctx.send(random.choice(lines))

    @commands.command(pass_context=True, name="knock",
                    description="Knock knock jokes are great", brief="Knock knock")
    async def randomfact(self, ctx):  # fact command
        with open("data/Knock_knock.txt", "r") as f:
            lines = f.readlines()
            await ctx.send(("Knock knock.|Who's there?|" + str(random.choice(lines))).replace("|", "\n"))

    @commands.command(pass_context=True, name="food",
                    description="Sends a random food item", brief="In case you get hungry",
                    aliases=["foods"])
    async def getfood(self, ctx):  # foods command
        db_interact.start()
        if db_interact.is_ascii(self, ctx.guild):
            with open("data/ascii_art.txt", "r") as f:
                lines = f.readlines()
                await ctx.send("```%s```" %random.choice(lines).replace("\\n", "\n"))
        else:
            await ctx.send("```Ascii art is disabled on this server idk why tho.```")
        db_interact.close()




class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="chat",
                    description="Set the channel for the in-game chat from channel name or id", brief="Set games chat channel")
    @has_permissions(administrator=True)
    async def chat(self, ctx, channel):  # chat command
        try:
            channel = client.get_channel(int(str(channel).replace("<", "").replace(">", "").replace("#", "")))
        except Exception as e:
            print(e)
        if str(channel).strip().lower() == "0" or str(channel).strip().lower() == "none":
                channel = lambda : print(end="")
                channel.id = 0
                channel.name = "None"
        db_interact.start()
        db_interact.update_channel(self, ctx.guild, channel.id)
        db_interact.close()
        await ctx.send("```Set in-game live chat to: %s```" %channel.name)

    @chat.error
    async def chat_error(error, ctx):
        await last.channel.send("```You do not have permission to do that!```")

    @commands.command(pass_context=True, name="prefix",
                    description="Set the bot prefix for the server", brief="Set prefix")
    @has_permissions(administrator=True)
    async def preffx(self, ctx, config=None):  # prefix command
        if config == None:
            await ctx.send("```A new prifix is required try help prefix```")
            return
        if len(config) ==1:
            await ctx.send("```Updated prefix to: %s```"%config)
            db_interact.start()
            db_interact.update_prefix(self, ctx.guild, config)
            db_interact.close()
            return
        else:
            await ctx.send("```Prifix must be 1 charecters long```")
        return


    @preffx.error
    async def preffx_error(self, ctx, error):
        await last.channel.send("```You do not have permission to do that!```")

    @commands.command(pass_context=True, name="ascii",
                    description="Configure ascii art allowance with [True/False]", brief="Allow ascii art")
    @has_permissions(administrator=True)
    async def ascii(self, ctx, config):  # ascii command
        db_interact.start()
        if config.lower().strip() == "true":
            await ctx.send("```Updated show ascii to True```")
            db_interact.update_ascii(self, ctx.guild, 1)
        if config.lower().strip() == "false":
            await ctx.send("```Updated show ascii to False```")
            db_interact.update_ascii(self, ctx.guild, 0)
        db_interact.close()
    @ascii.error
    async def ascii_error(error, ctx):
        await last.channel.send("```You do not have permission to do that!```")


class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="ticket",
                    description="Open ticket to pay for items", brief="Open ticket")
    async def ticket(self, ctx):  # confirm purchase command confirm
        if not is_ticket(self, ctx.message.channel):
            pass


def setup(client):
    client.add_cog(Information(client))
    client.add_cog(Utilities(client))
    client.add_cog(Spam(client))
    client.add_cog(Coins(client))
    client.add_cog(Fun(client))
    client.add_cog(Admin(client))
    client.add_cog(Shop(client))

setup(client)
client.run(sys.argv[1])
input("> ")
