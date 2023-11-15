from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from loger import loger


class OrderIdCallback(CallbackData, prefix="order_"):
    pk: str


def get_main_ikb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Все заказы'),
         KeyboardButton(text='Заказы сегодня')]])


def get_order_ikb(order: dict) -> InlineKeyboardMarkup:
    loger.debug(f'{order.get("id") = }')
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выполнен',
                              callback_data=OrderIdCallback(pk=str(order.get("id"))).pack()), ],
    ])
    return ikb
