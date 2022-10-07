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


@bot.tree.command(name="submit_result", description="To submit **your event's** winners and runners")
@app_commands.checks.has_any_role(1020308729796763669,1020316038178553937)
@app_commands.choices(
  position = [
    app_commands.Choice(name='Winner', value='FIRST'),
    app_commands.Choice(name='Runner', value='SECOND')
  ],
  event_name = [
    app_commands.Choice(name= "algocode", value= "ALGOCODE"),
    app_commands.Choice(name= "artistry", value= "ARTISTRY"),
    app_commands.Choice(name= "codesprint", value= "CODESPRINT"),
    app_commands.Choice(name= "colloquy", value= "COLLOQUY"),
    app_commands.Choice(name= "cybernerd", value= "CYBERNERD"),
    app_commands.Choice(name= "data-thon", value= "DATATHON"),
    app_commands.Choice(name= "eureka-paperpresentation", value= "EUREKA-PAPERPRESENTATION"),
    app_commands.Choice(name= "eureka-posterpresentation", value= "EUREKA-POSTERPRESENTATION"),
    app_commands.Choice(name= "flip-flop", value= "FLIP-FLOP"),
    app_commands.Choice(name= "fractalfanatic", value= "FRACTAL FANATIC"),
    app_commands.Choice(name= "hack-in", value= "HACK-IN"),
    app_commands.Choice(name= "inquizitives", value= "INQUIZITIVES"),
    app_commands.Choice(name= "invernirer", value= "INVERNIRER"),
    app_commands.Choice(name= "laststand-nfs", value= "LAST STAND-NFS"),
    app_commands.Choice(name= "laststand-valorant", value= "LAST STAND-VALORANT"),
    app_commands.Choice(name= "mathpirates", value= "MATH PIRATES"),
    app_commands.Choice(name= "nethunt", value= "NETHUNT"),
    app_commands.Choice(name= "reversecoding", value= "REVERSE CODING"),
    app_commands.Choice(name= "staroflogin2k22", value= "STAR OF LOGIN"),
    app_commands.Choice(name= "techiadz", value= "TECHIADZ"),
    app_commands.Choice(name= "thinklytics", value= "THINKLYTICS"),
    app_commands.Choice(name= "triple-trouble", value= "TRIPLE-TROUBLE")
  ]
) 
async def add_result(interaction: discord.Interaction, event_name: app_commands.Choice[str], participant_email: str, position: app_commands.Choice[str]):
  guild = bot.get_guild(interaction.guild_id)  
  user = guild.get_member(interaction.user.id)

  participant_name = db.get_user_name(registered_email=participant_email, conn=conn)

  if participant_name == "UserNameNotFound":
    await interaction.response.send_message("Participant not found! Please recheck Email ID")
    time.sleep(3)
    await interaction.delete_original_response()
    return
  await interaction.response.send_message("Your request has been submitted successfully!")
  em = discord.Embed(title=f"{event_name.value.title()} Winner Update",
                    description=f"Participant \t: {participant_name}\nEmail Address\t: {participant_email}\nPosition\t: {position.value}\n\n...has been updated!")

  payload={ 'email': f'{participant_email}',
            'event_name': f'{event_name.value}',
            'position': f'{position.value}'}
  files=[]
  headers = {}
  response = requests.request("POST", os.environ["RESULT_URL"], headers=headers, data=payload, files=files)
  f = open("test.html","w")
  f.write(response.text)
  f.close()
  
  if response.status_code == 200:
    await user.send(embed=em)
  else:
    await user.send("Your request has **NOT** been submitted please contact <@586862321922605076>")
  time.sleep(3)
  await interaction.delete_original_response()
  


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

