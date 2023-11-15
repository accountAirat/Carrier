from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from Controller import Controller
from .keyboards import OrderIdCallback, get_main_ikb, get_order_ikb
from bot.templates import order_template
from datetime import date


class BotHandlers:

    def __init__(self, controller: Controller, dp: Dispatcher):
        self.controller = controller
        self.dp = dp
        self.register_handlers()

    def register_handlers(self) -> None:
        self.dp.message.middleware()
        self.dp.message.register(self.cmd_start, Command('start', 'help'))
        self.dp.message.register(self.msg_delivery_kazan_orders, F.text == 'Все заказы')
        self.dp.message.register(self.msg_today_delivery_kazan_orders, F.text == 'Заказы сегодня')
        self.dp.callback_query.register(self.cl_order_update_status, OrderIdCallback.filter())
        self.dp.message.register(self.unprocessed)

    async def cmd_start(self, msg: types.Message) -> None:
        reply_text = f'Привет, {msg.from_user.first_name}!'

        await msg.answer(
            text=reply_text,
            reply_markup=get_main_ikb()
        )

    async def msg_today_delivery_kazan_orders(self, msg: types.Message) -> None:
        await self.msg_delivery_kazan_orders(msg=msg, delivery_date=date.today())

    async def msg_delivery_kazan_orders(self, msg: types.Message, delivery_date: date = None) -> None:
        orders = self.controller.orders(delivery_date)
        if not orders:
            await msg.answer(text='Заказов нет')

        for order in orders:
            await msg.answer(
                text=order_template(order=order),
                reply_markup=get_order_ikb(order),
                disable_web_page_preview=True,
            )

    async def cl_order_update_status(self, callback: types.CallbackQuery, callback_data: OrderIdCallback) -> None:
        if self.controller.order_completed(callback_data.pk):
            await callback.message.edit_text(text=callback.message.text + "\n<em>Выполнен</em>", parse_mode='HTML')
        else:
            await callback.message.reply("Статус заказа не изменился!")

    async def unprocessed(self, msg: types.Message):
        await msg.answer(f'Я не понял тебя!')
