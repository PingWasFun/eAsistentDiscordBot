import logging

from bot import bot
from setup import TOKEN

if __name__ == "__main__":
    log_level = logging.WARN
    fmt = (
        "[%(levelname)s] [%(filename)s]:%(lineno)s>[%(funcName)s]"
        " %(asctime)s - %(message)s "
    )
    logging.basicConfig(level=log_level, format=fmt)
    bot.run(TOKEN)
