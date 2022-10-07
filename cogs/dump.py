from imaplib import Commands
import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Dump(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name='dumplogs')
    async def dumplogs(self, message: discord.message.Message):
        log = open("./data/logs.txt", "a")
        await message.channel.send(file=discord.File("./data/logs.txt"))
        log.write(f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{ message.author.name}] requested log file.\n")
        log.close()
    
    @commands.command(name='dumplogst')
    async def dumplogs(self, message: discord.message.Message, arg):
        log = open("./data/logs.txt", "a")

        log_file = open("./data/logs.txt")
        logs = [log for log in log_file]
        count = int(arg)
        if int(arg) < len(logs):
            count = len(logs)
        send_logs = "```diff\n" + "\n".join(logs[-count:]) + "\n```"
        await message.channel.send(send_logs)

        log.write(f"--- [{datetime.now(pytz.timezone('Asia/Calcutta'))}] : [{ message.author.name}] requested log file.\n")
        log.close()

async def setup(bot):
    await bot.add_cog(Dump(bot))