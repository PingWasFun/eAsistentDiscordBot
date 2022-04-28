import logging

import discord
from discord.ext import commands

from setup import TOKEN


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botcogs = ["commands.schedule", "commands.util", "commands.config"]

    async def on_ready(self):
        logging.info(f"Logged in as {self.user}")

    async def setup_hook(self) -> None:
        for i in self.botcogs:
            await self.load_extension(i)
            logging.debug(f"Loaded {i}")
        await bot.tree.sync(guild=discord.Object(id=882993496141729792))


if __name__ == "__main__":
    log_level = logging.INFO
    fmt = (
        "[%(levelname)s] [%(filename)s]:%(lineno)s>[%(funcName)s]"
        " %(asctime)s - %(message)s "
    )
    logging.basicConfig(level=log_level, format=fmt)

    bot = Bot(
        command_prefix="<",
        intents=discord.Intents.all(),
        application_id=960173820352823376,
    )

    bot.run(TOKEN)
