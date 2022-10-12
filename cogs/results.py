import discord
from discord.ext import commands
from datetime import datetime
import requests
from discord import Embed, app_commands
import pytz
import time
import database.db as db, os

class Results(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.event_name_mapping = {'Algocode': 'ALGOCODE',
                                    'Eureka-paperpresentation': 'EUREKA-PAPERPRESENTATION',
                                    'Eureka-posterpresentation': 'EUREKA-POSTERPRESENTATION',
                                    'Datathon': 'DATATHON',
                                    'Hack-in': 'HACK-IN',
                                    'Last Stand-nfs': 'LAST STAND-NFS',
                                    'Last Stand-valorant': 'LAST STAND-VALORANT',
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

    @app_commands.command(name="submit_result", description="res")
    @app_commands.checks.has_any_role(1020308729796763669,1020316038178553937)
    @app_commands.choices(
    position = [
        app_commands.Choice(name='Winner', value='FIRST'),
        app_commands.Choice(name='Runner', value='SECOND')
    ]
    ) 
    async def add_result(self, interaction: discord.Interaction, participant_email: str, position: app_commands.Choice[str], sub_event: str = ""):
        guild = self.bot.get_guild(interaction.guild_id)  
        user = guild.get_member(interaction.user.id)
        conn = db.get_connection()

        user_roles = [role.name for role in user.roles if role.id !=1020308729796763669 and role.id !=1020316038178553937]

        participant_name = db.get_user_name(registered_email=participant_email, conn=conn)

        if participant_name == "UserNameNotFound":
            await interaction.response.send_message("Participant not found! Please recheck Email ID")
            time.sleep(3)
            await interaction.delete_original_response()
            return
        await interaction.response.send_message("Your request has been submitted successfully!")


        event_name = user_roles[1]

        if sub_event.lower() == "paper":
            event_name+="-paperpresentation"
        elif sub_event.lower() == "poster":
            event_name+= "-posterpresentation"
        elif sub_event.lower() == "nfs":
            event_name+="-nfs"
        elif sub_event.lower() == "valo":
            event_name+="-valorant"

        em = discord.Embed(title=f"{self.event_name_mapping[event_name].title()} Winner Update",
                            description=f"Participant \t: {participant_name}\nEmail Address\t: {participant_email}\nPosition\t: {position.value}")

        payload={ 'email': f'{participant_email}',
                    'event_name': f'{self.event_name_mapping[event_name]}',
                    'position': f'{position.value}'}
        files=[]
        headers = {}
        response = requests.request("POST", os.environ["RESULT_URL"], headers=headers, data=payload, files=files)
        f = open("test.html","w")
        f.write(response.text)
        f.close()

        em.set_footer(text=f"{response.text}")
        await user.send(embed=em)
        # channel = self.bot.get_channel(int(os.environ['RESULT_CHANNEL']))
        # await channel.send(embed=em)
        
        time.sleep(3)
        await interaction.delete_original_response()

    
    @add_result.error
    async def add_result_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            await interaction.response.send_message("https://tenor.com/SVf8.gif")
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