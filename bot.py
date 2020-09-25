import random
import os
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from challenge.func import *
client = commands.Bot(command_prefix='/')
import datetime
# Events:

from discord.ext import tasks
import sqlite3


@client.command()
#@commands.has_permissions(administrator=True)
@commands.has_any_role("Admin", "daddyPanda")
async def sendme(ctx):
    await ctx.author.send("You requested:", file=discord.File("cogs/database.db"))


'''@client.group(invoke_without_command=True)
async def welcome(ctx):
    await ctx.send("Available setup commands: \nwelcome channel <#channel>\nwelcome text <message>")

@welcome.command()
async def channel(ctx, channel:discord.TextChannel):
    if ctx.message.author.guild_permissions.manage_messages:
        db = sqlite3.connect('database')
        cursor = db.cursor()
        cursor.execute()'''

#####
@client.command()
@commands.has_role("daddyPanda")
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
@commands.has_role("daddyPanda")
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
@commands.has_role("daddyPanda")
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
#####



@client.event
async def on_ready():
    change_status.start()
    #send_db.start()
    ######

    ######
    print("Bot is Online!")

@tasks.loop(hours=24)
async def send_db():
    x = str(datetime.datetime.now())[:19]
    user = client.get_user(528182299821473802)
    await user.send(f"{x} ", file=discord.File("cogs/database.db"))

@tasks.loop(seconds=3600)
async def change_status():
    td = datetime.datetime(2020, 8, 15) - datetime.datetime.now()
    days, seconds = td.days, td.seconds
    hours = days * 24 + seconds // 3600
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f": {hours} hours remain untill I sleep for 7 days."))

@client.event
async def on_raw_reaction_add(payload):  # Participant role.
    if payload.emoji != discord.PartialEmoji(name="🖐️"):
        return
    if payload.channel_id == 736238486696493237:
        challenge_winner = discord.utils.get(payload.member.guild.roles, name="Challenge Winner")
        if challenge_winner in payload.member.roles:
            return
        participant = discord.utils.get(payload.member.guild.roles, name="Participant")
        await payload.member.add_roles(participant)


@client.event
async def on_message(message):
    #Test sever general ID:
    #submission_channel id: 733556852901675058
    #my: submission_channel = client.get_channel(723080313764315166)
    submission_channel = client.get_channel(733556852901675058)
    wrong_answer = client.get_channel(722701043149963268)
    is_only_ans = False
    if str(message.content)[0:4] == "DONT":
        return
    elif str(message.content)[0:3] == "ANS":
        is_only_ans = True

    if message.channel.id == 736176226833793044:

        response = message.content
        res = str(response)
        await message.delete()
        if res[0:3] == "```":
            response = response[3:-3]
        sarr = ["import os","import sys","import glob","pathlib","__import__","import time", "import pip"]
        '''safe = ("import os" not in res) and ("import sys" not in res) and ("import glob" not in res) and (
                "pathlib" not in res) and ("__import__" not in res) and ("import time" not in res) and (
                           "import pip" not in res)'''
        safe = True
        for ele in sarr:
            if ele in res:
                safe = False
        if safe:
            if message.author.bot: return
            else:
                mess = """"""
                error = False
                if is_only_ans:
                    with open("challenge/out.txt", "w") as f:
                        f.write(response[4:])
                else:
                    pen = response.split('\n')
                    solve(pen)
                    os.system('python challenge/t2.py < challenge/in.txt > challenge/out.txt')

                    file_path_out = 'challenge/out.txt'
                    file_path_log = 'challenge/log.txt'

                    mess = """"""
                    # check if size of file is 0
                    error = False
                    if os.path.getsize(file_path_out) == 0:
                        if os.path.getsize(file_path_log) == 0:
                            mess = "Syntax Error"
                        else:
                            with open("challenge/log.txt", "r") as f:
                                word = ", line "
                                for line in f:
                                    found = line.find(word)
                                    if found == -1:
                                        mess += line
                                    else:
                                        final = f"{line[:found+7]} {int(line[found+7]) - 3}{line[found+8:]}"
                                        mess+=final
                        error = True

                cans = ""
                cout = ""
                with open("challenge/answers.txt", "r") as f:
                    for line in f:
                        cans += str(line).rstrip()
                with open("challenge/out.txt", "r") as f:
                    for line in f:
                        cout += str(line).rstrip()
                cans = cans.rstrip()
                cout = cout.rstrip()

                val = cans == cout
                answer = False
                if val:
                    mess = f"ACCEPTED"
                    answer = True
                elif error==False:
                    mess = f"WRONG ANSWER"
                    answer = False


                if answer:
                    if is_only_ans:
                        embed = discord.Embed(description=f"```py\n{response[4:]}```\nYour Output: ```py\n{mess}```")
                    else:
                        embed = discord.Embed(description=f"```py\n{message.content}```\nYour Output: ```py\n{mess}```")
                    embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                    embed.set_footer(text=f'#ID: {message.author.id}')
                    await submission_channel.send(embed=embed)

                    participant = discord.utils.get(message.author.guild.roles, name="Participant")
                    challenge_winner = discord.utils.get(message.author.guild.roles, name="Challenge Winner")

                    if challenge_winner not in message.author.roles:
                        await message.author.add_roles(challenge_winner)
                        await message.author.remove_roles(participant)

                else:
                    embed = discord.Embed(description=f"\nYour Output: ```py\n{mess}```")
                    embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                    embed.set_footer(text=f'#ID: {message.author.id}')
                    await wrong_answer.send(embed=embed)
                '''file = open("challenge/out.txt", "w")
                file.close()
                file = open("challenge/log.txt", "w")
                file.close()'''
        else:
            await submission_channel.send(f"Forbidden Commands used by: {message.author}")
    await client.process_commands(message)

def solve(pen):
    ex = """except Exception as e:\n\ttraceback.print_exc(file=log)\n"""
    with open("challenge/t2.py", "w+") as file:
        text = "\n\t".join(pen)
        #print(text)
        file.write("""import traceback\nlog = open("challenge/log.txt", "w")\n""")
        file.write("try:\n\t")
        file.writelines(text)
        file.write('\n')
        file.write(ex)
        file.write("log.close()")

def psolve(pen):
    ex = """except Exception as e:\n\ttraceback.print_exc(file=log)\n"""
    with open("t1.py", "w+") as file:
        text = "\n\t".join(pen)
        #print(text)
        file.write("""import traceback\nlog = open("plog.txt", "w")\n""")
        file.write("try:\n\t")
        file.writelines(text)
        file.write('\n')
        file.write(ex)
        file.write("log.close()")


@client.command()
#@commands.has_permissions(administrator=True)
@commands.has_any_role("Dev", "Admin")
async def addquestion(ctx):
    """Admin command to add a question"""
    def check(m):
        return m.author == ctx.author
    try:
        await ctx.send("Provide Valid Input contents: ")
        a = await client.wait_for('message', check=check, timeout=60)
        with open("challenge/in.txt", 'w') as inp:
            inp.writelines(str(a.content))
        await ctx.channel.purge(limit=2)
        await ctx.send("Provide valid answer to the input file: ")
        a = await client.wait_for('message', check=check, timeout=60)
        with open("challenge/answers.txt", 'w') as ans:
            ans.writelines(str(a.content))
        await ctx.channel.purge(limit=3)
    except asyncio.TimeoutError:
        return await ctx.send('Sorry, you took too long')


'''@client.command()
async def python(ctx, *,arg):
    """Run Simple python codes use: /python xyz"""
    author = ctx.author

    sarr = ["import os", "import sys", "import glob", "pathlib", "__import__", "import time", "import pip"]


    res = str(arg)
    safe = True
    for ele in sarr:
        if ele in res:
            safe = False
            break
    if safe:
        if "input(" in str(arg):
            await ctx.send("Provide Valid Input contents: ")
            def check(m):
                return m.author == author
            try:
                a = await client.wait_for('message', check=check, timeout=30)
                with open("pin.txt", 'w') as inp:
                    inp.writelines(str(a.content))
            except asyncio.TimeoutError:
                return await ctx.send('Sorry, you took too long')
        pen = arg.split('\n')
        psolve(pen)
        os.system('python t1.py < pin.txt > pout.txt')
        mess = """"""
        file_path_out = 'pout.txt'
        file_path_log = 'plog.txt'
        # check if size of file is 0
        if os.path.getsize(file_path_out) == 0:
            if os.path.getsize(file_path_log) == 0:
                mess = "There is some Error in your code"
            else:
                with open("plog.txt", "r") as f:
                    for line in f:
                        mess += line
        else:
            with open("pout.txt", "r") as f:
                for line in f:
                    mess += line
        if ("bot.py" in mess) or ("NzIyNjk5MzY0NjM" in mess):
            await ctx.send("Nice try!")
        else:
            embed = discord.Embed(description=f"Your Output: ```py\n{mess}```")
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            # embed.set_footer(text=f'#ID: {ctx.author.id}')
            await ctx.send(embed=embed)

        file = open("pout.txt", "w")
        file.close()
        file = open("plog.txt", "w")
        file.close()
        file = open("pin.txt", "w")
        file.close()
    else:
        await ctx.send("Forbidden Commands")

'''

# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send("Wrong command!/you don't have permissions to use this command")


# Commands:

@client.command()
async def ping(ctx):
    """Test command to check bot's response time"""
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")



@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    """Admin command to clear chats, e.g. clear(10), erases 10 messages"""
    await ctx.channel.purge(limit=amount)


hellos = ['Howdy!', 'Hey there', 'Aloha', 'Bonjour', 'Hi']


@client.command(aliases=["sayhi"])
async def sayHi(ctx):
    """Says Hi to you"""
    await ctx.send(f"{random.choice(hellos)} {ctx.author.mention}!")


@client.command(aliases=["sayhito"])
async def sayHito(ctx, member):
    """Say Hi to a mentioned member"""
    await ctx.send(f"{random.choice(hellos)} {member}!")


@client.command(aliases=["answerme", "8ball"])
async def _8ball(ctx, *, question):
    """Classic 8 ball game, use: /answerme question"""
    responses = ['It is certain', 'Without a doubt', 'Yes – definitely', 'You may rely on it',
               'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'My Reply is hazy', 'try again',
               'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
               'Dont count on it', 'My reply is no', 'My sources say no', 'Very doubtful']
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


#test bot
client.run(TOKEN)