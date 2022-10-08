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
          log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is a Registered Participant\n")

          if "laststand-valorant" in events:
            roles.append(discord.utils.get(guild.roles, id=eventRoleMapping["ls-valorant"]))
          if "laststand-nfs" in events:
            roles.append(discord.utils.get(guild.roles, id=eventRoleMapping["ls-nfs"]))

        else:
          await user.send("Thank you for registering! However, we notice that you have not registered for Last Stand event. Please register for any event of your choice! You will have to submit your registered email ID again for this purpose. If you have any queries with regard to this, feel free to reach out to the <#1020390088200437760> channel or <#1025079500343607346> by tagging registration team or the server admin.\n\n Website : https://www.psglogin.in\n\nIf you have registered for other events from Login'22 please join our **Login'22 Discord Server** at https://discord.com/invite/RTrVjqMYF8")
        
        nickname = db.get_user_name(message.content, conn).title()
        await user.edit(nick=nickname)
        log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t User Nickname changed from '{user.display_name}' to {nickname}\n")

        await user.edit(roles=[])
        await user.add_roles(*roles)
        log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} added roles {roles}\n")
      
      else :
        log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is a Registered Participant\n")

        roles = [discord.utils.get(guild.roles, id=eventRoleMapping["participant"])]
        
        for event in events:
          roles.append(discord.utils.get(guild.roles, id=eventRoleMapping[event]))

      nickname = db.get_user_name(message.content, conn).title()
      await user.edit(nick=nickname)
      log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t User Nickname changed from '{user.display_name}' to {nickname}\n")
      
      await user.edit(roles=[])
      await user.add_roles(*roles)
      role_names = "\n".join(role.name for role in roles) 
      role_names = role_names.replace("Participants","")
      msg = f"Thank you for registering!\nHere is the list of Events you have registered : \n{role_names}"
      if message.guild.id == int(os.environ['LAST_STAND_GUILD']):
        msg = f"Thank you for registering!\nHere is the list of Events you have registered from Last Stand : \n{role_names}"
      await user.send(msg)
      log.write(f"[{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t{message.content} added roles {roles}\n")
    
    else:
      log.write(f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` has not registered any events\n")
      await user.send("Thank you for registering! However, we notice that you have not registered for any specific event. Please register for any event of your choice! You will have to submit your registered email ID again for this purpose. If you have any queries with regard to this, feel free to reach out to the <#1020388821742927932> channel or <#1025079557117710436> by tagging registration team or the server admin.\n\n Website : https://www.psglogin.in")
  
  else:
    userRegistered = db.get_alumni(message.content, conn)
    if userRegistered == "UserNameNotFound":
      log.write(f"- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{message.guild.name}] [{user.name}] \t`{message.content}` is Not A Registered Participant\n")
      await user.send("Oh ooh! We notice that you have not registered Login'22. Please register for any event of your choice! You will have to submit your email ID again for this purpose. If you have any queries with regard to this, feel free to reach out to the <#1020388821742927932> channel or <#1025079557117710436> or the server admin.\n\n Website : https://www.psglogin.in")
      return 0
    else:
      return 1
  return 0