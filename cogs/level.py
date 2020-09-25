import discord
from discord.ext import commands
import sqlite3
import math
class Level(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user and not str(message.content).startswith('/'):
            bots = discord.utils.get(message.author.guild.roles, name="bot buddies")
            tle = discord.utils.get(message.author.guild.roles, name="TLE")
            if bots in message.author.roles or tle in message.author.roles:
                return
            if message.channel.id != 723080313764315166 and message.channel.id != 722701043149963268:
                return
            db = sqlite3.connect('cogs/database.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = {message.guild.id} and user_id = {message.author.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO levels(guild_id, user_id, xp,lvl) VALUES(?,?,?,?)")
                val = (message.guild.id, message.author.id, 2, 1)
                cursor.execute(sql, val)
                db.commit()
            else:
                cursor.execute(f"SELECT user_id,xp,lvl FROM levels WHERE guild_id = {message.guild.id} and user_id = {message.author.id}")
                result1 = cursor.fetchone()
                exp = int(result1[1])
                sql = ("UPDATE levels SET xp = ? WHERE guild_id = ? and user_id = ?")
                val = (exp + 2 + math.floor(len(str(message.content))*0.03), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(
                    f"SELECT user_id,xp,lvl FROM levels WHERE guild_id = {message.guild.id} and user_id = {message.author.id}")
                result2 = cursor.fetchone()
                xp_start = int(result2[1])
                lvl_start = int(result2[2])
                #xp_end = math.floor(5 * (lvl_start)**0.5 + 50*lvl_start +100)
                xp_end = math.floor(200*lvl_start)
                if xp_end < xp_start:

                    await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start+1}!")
                    if lvl_start+1 == 5:
                        await message.channel.send(f"> Congratulations! You're hence pronounced an `Active Member`")
                        active_member = discord.utils.get(message.author.guild.roles, name="Active Coder")
                        if active_member not in message.author.roles:
                            await message.author.add_roles(active_member)


                    sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                    val = (int(lvl_start+1), str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()

                    sql = ("UPDATE levels SET xp = ? WHERE guild_id = ? and user_id = ?")
                    val = (0, str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('cogs/database.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = {ctx.message.guild.id} and user_id = {user.id}")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user is not yet ranked")
            else:
                embed = discord.Embed(
                    description=f"```py\n{user.name} is currently on level `{str(result[2])}` and has `{str(result[1])} XP\nXP needed for next level: {int(result[2])*200 - int(result[1])}```")
                await ctx.send(embed=embed)
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('cogs/database.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = {ctx.message.guild.id} and user_id = {ctx.message.author.id}")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user is not yet ranked")
            else:
                embed = discord.Embed(
                    description=f"```py\n{ctx.author.name} is currently on level {str(result[2])} and has {str(result[1])} XP\nXP needed for next level: {int(result[2])*200 - int(result[1])}```")
                await ctx.send(embed=embed)
    @commands.command()
    async def rankhelp(self, ctx):

        embed = discord.Embed(description=f"```py\nBe active in the server to gain XP.\nLevel 1: Just Typed Hello World!\nLevel 5: Active Coder(You get a new role)\nLevel 10: Orz```")
        await ctx.send(embed=embed)

    @commands.command()
    async def rank_list(self, ctx):
        """Displays top 10 Active Members in the server"""
        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT user_id,lvl FROM levels WHERE guild_id = {str(614871520275333120)} ORDER BY lvl DESC")
        res = cursor.fetchmany(10)
        #0: user_id, 1: lvl
        mess = "Top 10 members:\n"
        mess += "{: <5} {: <25} {: <3}\n".format("Rank", "User", "Level")
        x = 1
        for ele in res:
            #user = self.client.get_user(int(ele[0]))
            mess += "{: <5} {: <25} {: <3}\n".format(x,ele[0],ele[1])
            x+=1
        await ctx.send(f"```py\n{mess}```")


def setup(client):
    client.add_cog(Level(client))