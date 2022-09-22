from asyncio.log import logger
from http import server
import discord
from dotenv import load_dotenv, find_dotenv
import os
import json
from datetime import datetime
import re
import server

log = open("./data/logs.txt","a")

load_dotenv(find_dotenv())

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    log.write(f"[{datetime.now()}] Bot logged in\n")


async def add_role_member(message: discord.message.Message):

    guild =  bot.get_guild(message.guild.id)
    user =  guild.get_member(message.author.id)

    log.write(f"[{datetime.now()}] : {message.content} is a PSG Studentv")
    log.write(f"[{datetime.now()}] : Message Deleted '{message.content}' from {message.channel.name}\n")
    
    
    fp=open("./data/role_list.json", "r")
    data = json.load(fp=fp)

    
    if message.content.upper() in data.keys():

        nickname = data[message.content.upper()]["name"]
        log.write(f"[{datetime.now()}] : User Nickname changed from '{user.display_name}' to {nickname}\n")
        await user.edit(nick=nickname)
        
        roles =  [discord.utils.get(guild.roles, name=role_name) for role_name in data[message.content.upper()]["roles"]]
        await user.add_roles(*roles, reason=f"Role [{roles}] assigned upon on request")

        log.write(f"[{datetime.now()}] : {message.content} added roles {roles}\n" )

    else:

        await user.send("Your request cannot be processed. Either you are not a part of Login 2022 or your data is not available in the database. Please contact your Event Coordinator or Admin to gain access")
        log.write(f"[{datetime.now()}] : {message.content} Not available in database\n" )


async def add_role_participant(message: discord.message.Message):
    guild =  bot.get_guild(message.guild.id)
    user =  guild.get_member(message.author.id)
    log.write(f"[{datetime.now()}] : Message Deleted '{message.content}' from {message.channel.name}\n")
    log.write(f"[{datetime.now()}] : {message.content} is a Registered Participant\n")
    log.write(f"[{datetime.now()}] : {message.content} is a Not a Registered Participant\n")
    await user.send("Your haven't registered for Login 2022. Please Register through our website and try again later!.") 
    pass

@bot.event
async def on_message(message: discord.message.Message):
    if message.author == bot.user:
        return 

    if message.channel.id == 1021331433039605781:
        await message.delete()
        if re.match(r"\d{2}\w{2}\d+",message.content.upper()):
            await add_role_member(message=message)
        elif re.match(r".*@\w+\.+\w+", message.content):
            await add_role_participant(message=message)
        else:
            log.write(f"[{datetime.now()}] : Message Deleted '{message.content}' from {message.channel.name}\n")




if __name__ == "__main__":
    # server.start()
    bot.run(os.getenv("BOT_TOKEN"))
