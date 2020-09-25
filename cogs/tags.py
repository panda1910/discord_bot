import discord
from discord.ext import commands
import math
import asyncio
import sqlite3
class tags(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command()
    @commands.has_any_role("Admin", "daddyPanda", "Active Coder")
    async def add_tag(self, ctx, *,arg):
        author = ctx.author
        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        sql = (f"SELECT user_id FROM tags WHERE guild_id = ? and name = ?")
        val = (str(ctx.guild.id), str(arg).lower())
        cursor.execute(sql, val)
        rr = cursor.fetchone()
        if rr is None:
            def check(m):
                return m.author == author
            try:
                await ctx.send("Enter tag contents or prefix the message with NO to cancel: ")
                a = await self.client.wait_for('message', check=check, timeout=60)
                content = str(a.content)
                if content[:2] != "NO":
                    sql = ("INSERT INTO tags(data,guild_id, user_id, name) VALUES(?,?,?,?)")
                    val = (a.content,ctx.guild.id, ctx.author.id, str(arg))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    await ctx.send("Tag successfully created!")
                else:
                    await ctx.send('Tag Cancelled', delete_after=3.0)
                    cursor.close()
                    db.close()
                    return
            except asyncio.TimeoutError:
                cursor.close()
                db.close()
                return await ctx.send('Sorry, you took too long')
        else:
            cursor.close()
            db.close()
            await ctx.send("Tag already exists Use update instead")



    @commands.command()
    @commands.has_any_role("Admin", "daddyPanda", "Active Coder")
    async def update_tag(self, ctx, *, arg):
        author = ctx.author
        name = str(arg)

        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        sql = (f"SELECT name,user_id,data FROM tags WHERE guild_id = ? and name = ?")
        val = (str(ctx.guild.id), str(arg).lower())
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is None:
            await ctx.send("Tag does not exist", delete_after=3.0)
        else:
            def check(m):
                return m.author == author
            try:
                await ctx.send("Enter new data or prefix the message with NO to cancel: ")
                a = await self.client.wait_for('message', check=check, timeout=60)
                content = str(a.content)
                if content[:2] != "NO":
                    db = sqlite3.connect('cogs/database.db')
                    cursor = db.cursor()
                    sql = (f"UPDATE tags SET data = ? WHERE guild_id = ? and name = ?")
                    val = (content, ctx.guild.id, name)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    await ctx.send("Tag successfully updated!")
                else:
                    await ctx.send('Tag Cancelled', delete_after=3.0)
                    return
            except asyncio.TimeoutError:
                return await ctx.send('Sorry, you took too long')

    @commands.command()
    @commands.has_any_role("Admin", "daddyPanda")
    async def del_tag(self, ctx, *, arg):
        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        sql = (f"SELECT rowid,user_id,data FROM tags WHERE guild_id = ? and name = ?")
        val = (str(ctx.guild.id), str(arg).lower())
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is not None:
            sql = (f"DELETE FROM tags WHERE rowid = ?")
            val = (str(result[0]))
            cursor.execute(sql, val)
            await ctx.send("Tag successfully deleted!")
            db.commit()
        else:
            await ctx.send("No tags found")
        cursor.close()
        db.close()

    @commands.command()
    async def tag(self, ctx, *, arg):
        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        sql = (f"SELECT rowid,name,data FROM tags WHERE guild_id = ? and name = ?")
        val = (str(ctx.guild.id), str(arg).lower())
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is not None:
            await ctx.send(f"{result[2]}")
        else:
            await ctx.send("No tags found")
        cursor.close()
        db.close()

    @commands.command()
    async def list_tags(self, ctx):
        db = sqlite3.connect('cogs/database.db')
        cursor = db.cursor()
        cursor.execute("SELECT rowid, * FROM tags")
        items = cursor.fetchall()
        mess = ""
        i = 1
        for ele in items:
            mess+= f"{i}: {ele[2]}\n"
            i+=1

        await ctx.send(f"```py\nCall as:\n/tag <name>\n{mess}```")
        cursor.close()
        db.close()


def setup(client):
    client.add_cog(tags(client))