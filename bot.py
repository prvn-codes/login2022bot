import discord
import os
from datetime import datetime
import re
import database.db as db
import pytz
from utils.add_role_member import addRoleMember
from utils.add_role_participant import addRoleParticipant
from utils.add_role_aumni import addRoleAlumni
from discord.ext import commands
import asyncio
from discord import Status, app_commands
import time
import requests

# import set_environs
# set_environs.setup_environs()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

conn = db.get_connection()


@bot.event
async def on_ready():
  log = open("./data/logs.txt", "a")
  
  try:
    synced = await bot.tree.sync()
    log.write(f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}]: [bot] Bot synced {synced}\n")
  except Exception as e:
    log.write(f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}]: [bot] Bot not synced {e}\n")

  await bot.change_presence(activity=discord.Game(name="https://www.psglogin.in"))
  
  log.write(f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}]: [bot] Bot logged in\n")
  log.close()
  


@bot.event
async def on_message(message: discord.message.Message):

  log = open("./data/logs.txt", "a")

  if message.author == bot.user:
    return

  if message.channel.id == int(os.environ["LOGIN_CHANNEL_ID"]) or message.channel.id == int(os.environ["LAST_STAND_CHANNEL_ID"]):
    await message.delete()
    log.write(f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{bot.get_user(message.author.id).name}] \tMessage Deleted `{message.content}`\n")
    
    if re.match(r".*@\w+\.+\w+", message.content):
      res = await addRoleParticipant(bot=bot, message=message, log=log, conn=conn)
      if res:
        await addRoleAlumni(bot=bot, message=message, conn=conn)
    
    elif re.match(r"\d{2}\w{2}\d+", message.content.upper()):
      await addRoleMember(bot=bot, message=message, log=log)
    
    
    else:
      pass

  log.close()
  await bot.process_commands(message)




async def load_cogs_func():
  print("--- Loading Cogs ---")
  for _, _, files in os.walk('./cogs/'):
        for file in files:
            file_name, ext = os.path.splitext(file)
            print(f"{file_name}")
            await bot.load_extension(f'cogs.{file_name}')
        break
  print("---Cogs Loaded---")   


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(load_cogs_func())
  bot.run(os.environ["BOT_TOKEN"])
  loop.close()

