import discord
import os
from datetime import datetime
import pytz
import json

fp = open("./data/userrolemapping.json", "r")
userRoleMapping = json.load(fp=fp)
fp.close()

fp = open("./data/eventRoleMapping.json", "r")
eventRoleMapping = json.load(fp=fp)
fp.close()

fp = open("./data/lsuserrolemapping.json", "r")
lsuserrolemapping = json.load(fp=fp)
fp.close()

async def addRoleMember(bot, message: discord.message.Message, log):
  guild = bot.get_guild(message.guild.id)
  user = guild.get_member(message.author.id)

  log.write(
    f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} is a PSG Student\n"
  )

  if message.content.upper() in userRoleMapping.keys():

    nickname = f'{userRoleMapping[message.content.upper()]["name"]}'
    if userRoleMapping[message.content.upper()]["event"] != "":
      nickname += " | " + userRoleMapping[message.content.upper()]["event"].replace(" - Nfs","").replace(" - Valorant","").replace(" - Poster Presentation","").replace(" - Paper Presentation","")

    await user.edit(nick=nickname)
    log.write(
      f"+ [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t User Nickname changed from '{user.display_name}' to {nickname}\n"
    )


    if message.guild.id == int(os.environ["LAST_STAND_GUILD"]):
      roles = [
        discord.utils.get(guild.roles, id=role_id)
        for role_id in lsuserrolemapping[message.content.upper()]["roles"]
      ]
    else:
      roles = [
        discord.utils.get(guild.roles, id=role_id)
        for role_id in userRoleMapping[message.content.upper()]["roles"]
      ]
    await user.edit(roles=[])
    await user.add_roles(*roles,
                         reason=f"Role [{roles}] assigned upon on request")

    log.write(
      f"+ [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} added roles {roles}\n"
    )

  else:

    await user.send(
      "Your request cannot be processed. Please contact your Event Coordinator or Admin to gain access"
    )
    log.write(
      f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} Not available in database\n"
    )