import asyncio
import betterlogging as logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from apps.hendlers import router
from middlewares.throttling import ThrottlingMiddleware

load_dotenv()

dp = Dispatcher()


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'),)
    dp.message.middleware(ThrottlingMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basic_colorized_config(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
        datefmt='%H:%M:%S'
    )
    asyncio.run(main())
