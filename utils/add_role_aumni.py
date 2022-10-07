import discord
import os
from datetime import datetime
import database.db as db

async def addRoleAlumni(bot, message: discord.message.Message, conn: db):
    guild = bot.get_guild(message.guild.id)
    user = guild.get_member(message.author.id)
    userRegistered = db.get_alumni(message.content, conn)
    
    if userRegistered != "UserNameNotFound":
        if guild.id == int(os.environ['LAST_STAND_GUILD']):
            user.send("Welcome Alumni")
            return
        await user.edit(nick=userRegistered.title())
        await user.edit(roles=[])
        roles = [discord.utils.get(guild.roles, name="Alumni")]
        await user.add_roles(*roles)
    


    
    
