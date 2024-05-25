from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import apps.keyboard as kb
from apps.search import search_query


router = Router()

type_movies = {'film': 'Фильм', 'series': 'Сериал'}


class Params(StatesGroup):
    type_movie = State()
    name = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Добро пожаловать, " +
                         f"<b>{message.from_user.full_name}</b> 😎",
                         parse_mode="html", reply_markup=kb.find_movie)


@router.message(F.text == 'Найти')
async def movie_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Params.type_movie)
    await message.answer('Укажите фильм или сериал вы ищите',
                         reply_markup=kb.choice)


@router.callback_query(F.data == 'series')
async def series_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.update_data(type_movie='series')
    await state.set_state(Params.name)
    await callback.message.answer(f'Введите название')


@router.callback_query(F.data == 'film')
async def film_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.update_data(type_movie='film')
    await state.set_state(Params.name)
    await callback.message.answer(f'Введите название')


@router.message(Params.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    data = await state.get_data()
    movie = search_query(data['name'].capitalize(), data['type_movie'])
    await message.answer(f"Название: <b>{data['name']}</b>\n" +
                         f"Тип: <b>{type_movies[data['type_movie']]}</b>",
                         parse_mode="html")
    if movie:
        await message.answer("По вашему запросу найдено ✨✨✨:")
        await message.answer_photo(photo=movie['picture'],
                                   caption=f"<b>{movie['title']}</b>\n" +
                                           f"{movie['description']}\n" +
                                           f"{movie['link']}",
                                   parse_mode="html")
    else:
        await message.answer(f"Ваш {type_movies[data['type_movie']]} " +
                             f"не найден 😢")
    await message.answer('Найти новый фильм?', reply_markup=kb.find_movie)
