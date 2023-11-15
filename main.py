import retailcrm

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.methods import SetMyCommands

from loger import loger
from settings import CRM_URL, CRM_TOKEN, BOT_TOKEN, PARSE_MODE

from crm.CrmService import CrmService
from Controller import Controller
from bot.BotHandlers import BotHandlers


async def main() -> None:
    client = retailcrm.v5(crm_url=CRM_URL, api_key=CRM_TOKEN)
    crm = CrmService(client)
    controller = Controller(crm)

    bot = Bot(BOT_TOKEN, parse_mode=PARSE_MODE)
    dp = Dispatcher()
    dp.startup.register(on_startup)

    bot_handlers = BotHandlers(controller, dp)
    bot_handlers.register_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=[BotCommand(command="start", description="it is start command...")])

    try:
        await dp.start_polling(bot)
    except Exception as e:
        loger.critical(e)


async def on_startup():
    loger.info('#################### SERVER_START ####################')


if __name__ == '__main__':
    asyncio.run(main())
