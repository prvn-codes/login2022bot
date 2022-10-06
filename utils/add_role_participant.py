import discord
import os
from datetime import datetime
import database.db as db
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

async def addRoleParticipant(bot, message: discord.message.Message, log, conn):

  events = db.get_user_events(message.content, conn)
  guild = bot.get_guild(message.guild.id)
  user = guild.get_member(message.author.id)
  userRegistered = db.get_user_name(message.content, conn)

  if userRegistered != "UserNameNotFound":
    if events:
      if message.guild.id == int(os.environ["LAST_STAND_GUILD"]):
        roles = [discord.utils.get(guild.roles, id=eventRoleMapping["ls-participant"])]
        if ("laststand-valorant" in events) or "laststand-nfs" in events:
          log.write(
            f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is a Registered Participant\n"
          )

          if "laststand-valorant" in events:
            roles.append(discord.utils.get(guild.roles, id=eventRoleMapping["ls-valorant"]))
          if "laststand-nfs" in events:
            roles.append(discord.utils.get(guild.roles, id=eventRoleMapping["ls-nfs"]))
        else:
          await user.send(
            "Oh oohh!, it seems like you haven't registered for the event Last Stand, Login 2022. Please Register through our website and try again later! If this continues, please contact Server Admin\n\n Website : https://www.psglogin.in\n\nIf you have registered for other events from Login 2022 please join our **Login 2022 Discord Server** at https://discord.com/invite/RTrVjqMYF8"
          )
        nickname = db.get_user_name(message.content, conn).title()
        await user.edit(nick=nickname)
        log.write(
          f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t User Nickname changed from '{user.display_name}' to {nickname}\n"
        )

        await user.edit(roles=[])
        await user.add_roles(*roles,
                            reason=f"Role [{roles}] assigned upon on request")
        log.write(
          f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} added roles {roles}\n"
        )
      else :
        log.write(
        f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is a Registered Participant\n"
        )

        roles = [
          discord.utils.get(guild.roles, id=eventRoleMapping["participant"])
        ]
        for event in events:
          roles.append(discord.utils.get(guild.roles, id=eventRoleMapping[event]))

      nickname = db.get_user_name(message.content, conn).title()
      await user.edit(nick=nickname)
      log.write(
        f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t User Nickname changed from '{user.display_name}' to {nickname}\n"
      )
      await user.edit(roles=[])
      await user.add_roles(*roles,
                          reason=f"Role [{roles}] assigned upon on request")
      log.write(
        f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} added roles {roles}\n"
      )
    else:
      log.write(
        f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` has not registered any events\n"
      )
      await user.send(
        "Oh oohh!, it seems like you haven't registered any events from Login 2022. Please Register through our website and try again later! If this continues, please contact Server Admin\n\n Website : https://www.psglogin.in"
      )
  else:
    log.write(
        f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is Not A Registered Participant\n"
      )
    await user.send(
        "Oh oohh!, it seems like you haven't registered any events from Login 2022. Please Register through our website and try again later! If this continues, please contact Server Admin\n\n Website : https://www.psglogin.in"
      )