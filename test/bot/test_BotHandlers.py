import pytest
from unittest.mock import Mock, AsyncMock
from aiogram import Dispatcher

from src.bot.keyboards import get_main_ikb

from src.bot.BotHandlers import BotHandlers


@pytest.fixture
def controller():
    controller = Mock()
    return controller


@pytest.fixture
def bot_handlers(controller):
    return BotHandlers(controller=controller, dp=Dispatcher())


#
@pytest.fixture
def msg():
    msg = AsyncMock()
    msg.from_user.first_name = "Test_name"
    return msg


@pytest.mark.asyncio
async def test_cmd_start(msg, bot_handlers):
    await bot_handlers.cmd_start(msg=msg)
    msg.answer.assert_called_with(text=f'Привет, Test_name!', reply_markup=get_main_ikb())


@pytest.mark.asyncio
async def test_msg_delivery_kazan_orders(msg, bot_handlers):
    bot_handlers.controller.orders.side_effect = [None]
    await bot_handlers.msg_today_delivery_kazan_orders(msg=msg)
    msg.answer.assert_called_with(text='Заказов нет')


@pytest.mark.asyncio
async def test_unprocessed(msg, bot_handlers):
    await bot_handlers.unprocessed(msg=msg)
    msg.answer.assert_called_with("Я не понял тебя!")
