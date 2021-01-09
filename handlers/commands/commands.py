from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from loguru import logger

from keyboards.inline.cancel import cancel_button
from keyboards.inline.instagram import instagram_button
from loader import dp, db, bot
from keyboards.default.menu import menu_keyboard
from states.questions import Question
from texts.instagram import more_photo, instagram_link
from texts.question import question
from utils.chek_state import reset_state


@dp.message_handler(text="Примеры работ", state=["*"])
async def get_work_examples(message: types.Message, state: FSMContext):
    """Отправляем последние 5 фотографий и ссылку на инстаграм"""
    await reset_state(state, message)
    recent_photos = await db.get_instagram_pictures()
    media = [InputMediaPhoto(photo_url) for photo_url in recent_photos]
    await bot.send_media_group(message.from_user.id, media)
    await message.answer(more_photo, reply_markup=menu_keyboard)


@dp.message_handler(text="Instagram", state=['*'])
async def get_instagram_link(message: types.Message, state: FSMContext):
    """Отправляем кнопку с ссылкой на инстаграм"""
    await reset_state(state, message)
    await message.answer(instagram_link, reply_markup=instagram_button)


@dp.message_handler(text="Задать вопрос", state=['*'])
async def ask_a_question(message: types.Message, state: FSMContext):
    """Пользователь нажимает на кнопку задать вопрос"""
    await reset_state(state, message)
    mess = await message.answer(question, reply_markup=cancel_button)
    await state.update_data(message_id=mess['message_id'])
    await Question.WaitQuestion.set()