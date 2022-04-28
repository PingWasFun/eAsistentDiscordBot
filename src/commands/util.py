import logging

from discord.ext import commands


class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.debug(f"commands.util (UtilitiesCog) started")

    @commands.command(name="ping")
    @commands.is_owner()
    async def ping(self, ctx: commands.context.Context):
        await ctx.send(f"Pong")

    @commands.command(aliases=["shutdown"])
    @commands.is_owner()
    async def close(self, ctx: commands.context.Context):
        await ctx.send("Shutting down bot...")
        logging.warning(
            f"Bot shutdown from command. name: {ctx.author.name}"
            f"#{ctx.author.discriminator} ({ctx.author.display_name}), "
            f"id: {ctx.author.id}, guild: {ctx.guild.name}, guild ID: "
            f"{ctx.guild.id}"
        )
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(UtilitiesCog(bot))
