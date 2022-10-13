import discord
from discord.ext import commands
from datetime import datetime
import requests
from discord import Embed, app_commands
import pytz
import time
import database.db as db, os
import json, random

class Results(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.event_to_db_name_mapping = {'Algocode': 'ALGOCODE',
                                        'Eureka-paperpresentation': 'EUREKA-PAPERPRESENTATION',
                                        'Eureka-posterpresentation': 'EUREKA-POSTERPRESENTATION',
                                        'Datathon': 'DATATHON',
                                        'Hack-in': 'HACK-IN',
                                        'Last Stand-nfs': 'LASTSTAND-NFS',
                                        'Last Stand-valorant': 'LASTSTAND-VALORANT',
                                        'Triple Trouble': 'TRIPLE-TROUBLE',
                                        'Math Pirates': 'MATH PIRATES',
                                        'Reverse Coding': 'REVERSE CODING',
                                        'InQuizitives': 'INQUIZITIVES',
                                        'Artistry': 'ARTISTRY',
                                        'Code Sprint': 'CODESPRINT',
                                        'Colloquy': 'COLLOQUY',
                                        'Cybernerd': 'CYBERNERD',
                                        'Flip-Flop': 'FLIP-FLOP',
                                        'Fractal Fanatics': 'FRACTAL FANATIC',
                                        'Invenirer': 'INVENIRER',
                                        'Nethunt': 'NETHUNT',
                                        'Techiadz': 'TECHIADZ',
                                        'Star of Login': 'STAR OF LOGIN',
                                        'Thinklytics': 'THINKLYTICS'}
        self.db_to_event_name_mapping ={'ALGOCODE' : 'Algocode',
                                        'EUREKA-PAPERPRESENTATION' : 'Eureka',
                                        'EUREKA-POSTERPRESENTATION' : 'Eureka',
                                        'DATATHON' : 'Datathon',
                                        'HACK-IN' : 'Hack-in',
                                        'LASTSTAND-NFS' : 'Last Stand',
                                        'LASTSTAND-VALORANT' : 'Last Stand',
                                        'TRIPLE-TROUBLE' : 'Triple Trouble',
                                        'MATH PIRATES' : 'Math Pirates',
                                        'REVERSE CODING' : 'Reverse Coding',
                                        'INQUIZITIVES' : 'InQuizitives',
                                        'ARTISTRY' : 'Artistry',
                                        'CODESPRINT' : 'Code Sprint',
                                        'COLLOQUY' : 'Colloquy',
                                        'CYBERNERD' : 'Cybernerd',
                                        'FLIP-FLOP' : 'Flip-Flop',
                                        'FRACTAL FANATIC' : 'Fractal Fanatics',
                                        'INVENIRER' : 'Invenirer',
                                        'NETHUNT' : 'Nethunt',
                                        'TECHIADZ' : 'Techiadz',
                                        'STAR OF LOGIN' : 'Star of Login',
                                        'THINKLYTICS' : 'Thinklytics'}



    def get_vadivelu(self):
        memes = ["https://tenor.com/SVf8.gif",
                "https://tenor.com/SiRj.gif",
                "https://tenor.com/3Sg4.gif",
                "https://tenor.com/0iGY.gif",
                "https://tenor.com/bQLO5.gif",
                "https://tenor.com/IeJz.gif",
                "https://tenor.com/bkDwY.gif",
                "https://tenor.com/uwRs2fQj8T4.gif"
                ]
        return memes[random.randrange(0, len(memes))]

# ------------------------------------------------------------------------------------------ add -----------------------------------------------------------------------------------

    @app_commands.command(name="submit_result", description="To submit results of your event!")
    @app_commands.checks.has_any_role(1020308729796763669,1020316038178553937)
    @app_commands.choices(
    position = [
        app_commands.Choice(name='Winner', value='1'),
        app_commands.Choice(name='Runner', value='2')
    ]
    ) 
    async def add_results(self, interaction: discord.Interaction, participant_email: str, position: app_commands.Choice[str], sub_event: str = ""):
        
        await interaction.response.send_message("Your request has been submitted successfully!")
        
        guild = self.bot.get_guild(interaction.guild_id)  
        user = guild.get_member(interaction.user.id)
        conn = db.get_connection()

        user_roles = [role.name for role in user.roles if role.id !=1020308729796763669 and role.id !=1020316038178553937]

        participant_name = db.get_user_name(registered_email=participant_email, conn=conn)

        if participant_name == "UserNameNotFound":
            await interaction.edit_original_response(content="Participant not found! Please recheck Email ID")
            await user.send("Participant not found! Please recheck Email ID")

            time.sleep(6)
            await interaction.delete_original_response()
            return


        event_name = user_roles[1]

        if sub_event.lower() == "paper":
            event_name+="-paperpresentation"
        elif sub_event.lower() == "poster":
            event_name+= "-posterpresentation"
        elif sub_event.lower() == "nfs":
            event_name+="-nfs"
        elif sub_event.lower() == "valo":
            event_name+="-valorant"

        em = discord.Embed(title=f"{self.event_to_db_name_mapping[event_name].title()} Winner Update",
                            description=f"Participant \t: {participant_name}\nEmail Address\t: {participant_email}\nPosition\t: {position.value}")

        payload={ 'email': f'{participant_email}',
                    'event_name': f'{self.event_to_db_name_mapping[event_name]}',
                    'position': f'{position.value}'}
        files=[]
        headers = {}
        response = requests.request("POST", os.environ["RESULT_URL"], headers=headers, data=payload, files=files)
        res = json.loads(response.text)

        em.timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))
        em.set_footer(text=f"Result ID : {res['id']} | Message : {res['message']} | updated on ")
        await user.send(embed=em)
        # channel = self.bot.get_channel(int(os.environ['RESULT_CHANNEL']))
        # await channel.send(embed=em)
        
        time.sleep(3)
        await interaction.delete_original_response()

    
    @add_results.error
    async def add_result_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(self.get_vadivelu())
        else:
            print(error)

# ------------------------------------------------------------------------------------------ Edit -----------------------------------------------------------------------------------

    @app_commands.command(name="edit_result", description="edit submmitted result")
    @app_commands.checks.has_any_role(1020308729796763669,1020316038178553937)
    @app_commands.choices(
    position = [
        app_commands.Choice(name='Winner', value='1'),
        app_commands.Choice(name='Runner', value='2')
    ]
    ) 
    async def edit_results(self, interaction:discord.Interaction, result_id: int, participant_email: str, position:app_commands.Choice[str]):
        
        await interaction.response.send_message("Request to edit result has been submitted successfully")
        
        guild = self.bot.get_guild(interaction.guild_id)  
        user = guild.get_member(interaction.user.id)
        conn = db.get_connection()

        url = os.environ["RESULT_URL"]+'?id='+str(result_id)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        existing_result = json.loads(response.text)

        if existing_result['ERROR']:
            await interaction.edit_original_response(content=f"**Error :** {existing_result['ERROR']}")
            time.sleep(3)
            await interaction.delete_original_response()
            return

        user_roles = [role.name for role in user.roles if role.id !=1020308729796763669 and role.id !=1020316038178553937]

        if(self.db_to_event_name_mapping[existing_result["event_name"]] not in user_roles):
            await interaction.edit_original_response(content="Your are not authorised to submit this action!\n\nhttps://tenor.com/SVf8.gif")
            time.sleep(3)
            await interaction.delete_original_response()
            return

        participant_name = db.get_user_name(registered_email=participant_email, conn=conn)

        if participant_name == "UserNotFound":
            await interaction.edit_original_response(content="Incorrect Participant Email address, Recheck and try again")
            await user.send("Incorrect Participant Email address, Recheck and try again")
            return

        url = os.environ["RESULT_URL"]
        payload={'id': f'{result_id}',
                'position': f"{position.value}",
                'email': f'{participant_email}'}
        files=[

        ]
        headers = {}
        response = requests.request("PUT", url, headers=headers, data=payload, files=files)
        res = json.loads(response.text)

        em = discord.Embed(title=f"{existing_result['event_name'].title()} Winner Update",
                            description=f"Participant \t: {participant_name}\nEmail Address\t: {participant_email}\nPosition\t: {position.value}")
        em.timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))
        em.set_footer(text=f"Result ID : {result_id} | Message : {res['message']} | updated on ")
        
        await user.send(embed=em)

        time.sleep(6)
        await interaction.delete_original_response()

    @edit_results.error
    async def add_result_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(self.get_vadivelu())
        else:
            print(error)

# ------------------------------------------------------------------------------------------ Delete -----------------------------------------------------------------------------------

    @app_commands.command(name="delete_result", description="to delete a submmitted result")
    @app_commands.checks.has_any_role(1020308729796763669,1020316038178553937)
    async  def delete_results(self, interaction: discord.Interaction, result_id: int, reason : str = ""):

        await interaction.response.send_message("Request to delete result has been submitted successfully")
        
        guild = self.bot.get_guild(interaction.guild_id)  
        user = guild.get_member(interaction.user.id)

        conn = db.get_connection()


        url = os.environ["RESULT_URL"]+'?id='+str(result_id)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        existing_result = json.loads(response.text)
        print(existing_result)

        if 'ERROR' in existing_result.keys():
            await interaction.edit_original_response(content=f"**Error :** {existing_result['ERROR']}")
            time.sleep(3)
            await interaction.delete_original_response()
            return

        user_roles = [role.name for role in user.roles if role.id !=1020308729796763669 and role.id !=1020316038178553937]

        if(self.db_to_event_name_mapping[existing_result["event_name"]] not in user_roles):
            await interaction.edit_original_response(content="Your are not authorised to submit this action!\n\nhttps://tenor.com/SVf8.gif")
            time.sleep(3)
            await interaction.delete_original_response()
            return

        url = os.environ["RESULT_URL"]+"?id="+str(result_id)
        payload={}
        headers = {}

        response = requests.request("DELETE", url, headers=headers, data=payload)
        res = json.loads(response.text)

        participant_name = db.get_user_name(registered_email=existing_result['email'], conn=conn)
        em = discord.Embed(title=f"{existing_result['event_name'].title()} Winner Update",
                            description=f"Participant \t: {participant_name}\nEmail Address\t: {existing_result['email']}\nPosition\t: {existing_result['position']}")
        em.timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))
        em.set_footer(text=f"Result ID : {result_id} | Message : {res['message']} | updated on ")
        
        await user.send(embed=em)
        time.sleep(6)
        await interaction.delete_original_response()

    @delete_results.error
    async def add_result_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(self.get_vadivelu())
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(Results(bot))



'''event_name = [
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
    ]'''