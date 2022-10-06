import discord
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def _ping(self, ctx: commands.context.Context):
        em = discord.Embed(
            description=f":heart:  {int(self.bot.latency * 1000)}ms",
            color=0x15ead5
        )
        await ctx.send(embed=em)
    
async def setup(bot):
    await bot.add_cog(Utils(bot))
