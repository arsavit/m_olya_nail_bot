from aiogram import types
from loader import dp
from keyboards.default.menu import menu_keyboard


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(
        "Неизвестная команда. Вы можете воспользоваться командой /help, чтобы увидеть доступные команды.",
        reply_markup=menu_keyboard)
