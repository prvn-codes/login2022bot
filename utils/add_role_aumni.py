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
            # await user.send(f"As an esteemed alumni of our departments, we welcome you {userRegistered.title()}, whose constant source of encouragement and support has been the backbone of our growth over the years. It must be noted that our departments have always emphasized on the bond between the senior and junior batches on campus, and that this extends into all kinds of support, mentoring and avenues for learning even after graduation.\n\nPlease Join Login'22 discord server too. https://discord.com/invite/RTrVjqMYF8")
            return
        await user.edit(nick=userRegistered.title())
        await user.edit(roles=[])
        roles = [discord.utils.get(guild.roles, name="Alumni")]
        await user.add_roles(*roles)
        # await user.send(f"As an esteemed alumni of our departments, we welcome you {userRegistered.title()}, whose constant source of encouragement and support has been the backbone of our growth over the years. It must be noted that our departments have always emphasized on the bond between the senior and junior batches on campus, and that this extends into all kinds of support, mentoring and avenues for learning even after graduation.")


    
    
