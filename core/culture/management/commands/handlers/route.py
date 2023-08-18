import asyncio
import emoji
import io

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, ReplyKeyboardMarkup,
    ReplyKeyboardRemove, FSInputFile
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import text, italic, code
from django.core.exceptions import ObjectDoesNotExist
from speech_recognition.exceptions import UnknownValueError


from ..config import logger
from ..functions import (
    get_id_from_state, speech_to_text_conversion,
    get_exhibit_from_state,
    get_route_from_state
)

from ..crud import (
    save_review, get_exhibit,
    get_all_exhibits_by_route,
    get_routes_id, get_route_by_id
)
from ..utils import Route
from ..keyboards import (
    make_row_keyboard, KEYBOARD_YES_NO, make_vertical_keyboard
)
from .. import message as ms
from ..validators import rewiew_validator
from ..exceptions import FeedbackError

route_router = Router()

target = True


@route_router.message(Command("routes"))
async def command_start(message: Message, state: FSMContext) -> None:
    """Команда /routes . Предлагает выбрать маршрут."""
    # await message.reply(
    #     text=ms.CHOOSE_ROUTE_MESSAGE,
    #     reply_markup=make_row_keyboard(await get_routes_name()),
    # )
    keybord = []
    for route in await get_routes_id():
        keybord.append('Маршрут ' + str(route))
    await message.reply(
         text=ms.CHOOSE_ROUTE_MESSAGE,
         reply_markup=make_vertical_keyboard(keybord),
    )
    await state.set_state(Route.route)


@route_router.message(Route.route,  F.text.regexp(r'\d+'))
async def start_proute_number(message: Message, state: FSMContext) -> None:
    '''Поиск маршрута'''
    # проверка что введнный номер < len(route.exhibite.all())
    number = int(message.text) - 1
    await message.answer(
        f'Вы выбрали номер обекта={message.text}'
        f'Обьект расположен по адресу'
    )
    await state.update_data(exhibit_number=number)
    await message.answer(
        'Готовы перейти?',
        reply_markup=make_row_keyboard(['Да']),
        )
    route_id, exhibit_number = await get_id_from_state(state)
    exhibit = await get_exhibit(route_id, exhibit_number)
    await state.update_data(exhibit=exhibit)
    await state.set_state(Route.exhibit)


@route_router.message(Route.route,  F.text == "Нет")
async def start_route_no(message: Message, state: FSMContext) -> None:
    '''Поиск маршрута'''
    route = await get_route_from_state(state)
    await message.answer(f'Медитация начинается по адресу {route.address}')
    await message.answer(
        'Вы стоите в начале?',
        reply_markup=make_row_keyboard(['Да']),
        )


@route_router.message(Route.route,  F.text == 'Да')
async def start_route_yes(message: Message, state: FSMContext) -> None:
    '''Старт медитации'''
    await message.answer(
        'Отлично начнем нашу медитацию',
        reply_markup=make_row_keyboard(['Отлично начинаем'])
    )
    await state.set_state(Route.exhibit)


@route_router.message(Route.route)
async def route_info(message: Message, state: FSMContext) -> None:
    """Начало пути """
    route_id = message.text.split(' ')[-1]
    # try:
    #     await get_route_by_name(message.text.capitalize())
    # except ObjectDoesNotExist:
    #     logger.error(
    #                   'Пользователь ввел название маршрута,
    #                   которого нет в бд.'
    #       )
    #     await message.answer(
    #         'Выбери маршрут из тех, которые представлены на клавиатуре'
    #     )
    #     return
    try:
        route = await get_route_by_id(route_id)
    except ObjectDoesNotExist:
        logger.error('Пользователь ввел название маршрута, которого нет в бд.')
        await message.answer(
            'Выбери маршрут из тех, которые представлены на клавиатуре'
        )
        return
    await message.answer('Описания маршрута')
    await message.answer(
        f"Название маршрута {route.name}\n"
        f"Описание {route.description}\n"
    )
    await asyncio.sleep(1)
    image = FSInputFile(path='media/' + str(route.image))
    await message.answer_photo(image)
    # await state.update_data(route=message.text.capitalize())
    await state.update_data(route=route_id)
    await state.update_data(exhibit_number=0)

    exhibit = await get_exhibit(route_id, 0)
    await state.update_data(route_obj=route)
    await state.update_data(exhibit=exhibit)

    await message.answer(
        ms.START_ROUTE_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
    await message.answer('Если хотите выбрать номер обекта напишите его номер')


@route_router.message(
        Route.exhibit,
        F.text.in_({"Отлично! Идем дальше", "Yes", "Да", "Отлично начинаем"})
)
async def exhibit(message: Message, state: FSMContext) -> None:
    """
    Отрпавляет сообщение с экспонатом, запускается если
    есть состояние Route.exhibit и пользователь нажал
    на кнопку да(должно быть 'Отлично! Идем дальше' ??).
    Чек лист 4.7.1-4.7.2.
    """

    exhibit = await get_exhibit_from_state(state)
    print(exhibit)
    if exhibit.message_before_description != '':
        await message.answer(
            f"{exhibit.message_before_description}",
        )
    await message.answer(
        f"{exhibit.description}",
    )

    image = FSInputFile(path='media/' + str(exhibit.image))
    await message.answer_document(image)

    if exhibit.message_before_review != '':
        await message.answer(
            f"{exhibit.message_before_review}",
        )

    await asyncio.sleep(3)

    if exhibit.message_after_review != '':
        await message.answer(
            f"{exhibit.message_after_review}",
        )

    await message.answer(
        'Заполни отзыв на экспонат или что думаете?(фитч лист)',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Route.review)


@route_router.message(Route.review, F.text)
async def review(message: Message, state: FSMContext) -> None:
    '''Получения отзыва'''
    text = message.text
    await save_review(text, state)
    await message.answer('Спасибо за ваше наюддение')

    exhibit = await get_exhibit_from_state(state)

    route_id, exhibit_number = await get_id_from_state(state)
    exhibit_number += 1
    await state.update_data(exhibit_number=exhibit_number)
    route = await get_route_by_id(route_id)
    if exhibit_number == len(await get_all_exhibits_by_route(route)):
        await message.answer(
            'Конец маршрута',
            reply_markup=make_row_keyboard(['Конец']),
        )
        await state.set_state(Route.quiz)
    else:
        if exhibit.transfer_message != '':
            await message.answer(
                f"{exhibit.transfer_message}",
            )
        await message.answer(
            'Нас ждут длительные переходы',
            reply_markup=make_row_keyboard(['Отлично идем дальше']),
        )
        exhibit = await get_exhibit(route_id, exhibit_number)
        await state.update_data(exhibit=exhibit)
        await state.set_state(Route.transition)


@route_router.message(Route.review, F.voice)
async def get_voice_review(message: Message, state: FSMContext):
    '''
    Обработка голосового отзыва.
    1. Функция запускается если Route.review is True & F.voice is True.
        Временно перехватывает все голосовые.
    2. Получаем текст из аудио. Планирую через speech recognition.
            Текст получен.
    3. Вызываем валидатор для проверки, что сообщение соответствует критериям.
        Возможные критерии: сообщение не пустое, в сообщение минимум N слов,
                            сообщение не может состоять только из цифр,
                            мат(если получится).
            Валидатор готов.
    4. Если проверка не пройдена формируем ответ о проблеме с рекомендациями,
        что исправить.
            В случае ошибки райзится исключение. Из него забираем сообщение
            и передаем его пользователю в ответе.
    5. Вызываем функцию для сохранения отзыва в БД.
            В функцию передаём текст и модель юзера.
    6. Формируем ответ типа Спасибо за отзыв.
            Если не возникло ошибок передаем в ответ сообщение об успехе.
    7. Выводим кнопки дальнейших действий или предлагаем ввод текстовых
        команд. Зависит от бизнес-логики.
    '''
    answer = ''
    voice_file = io.BytesIO()
    await message.bot.download(
        message.voice,
        destination=voice_file
    )
    try:
        text = await speech_to_text_conversion(filename=voice_file)
    except UnknownValueError:
        answer = 'Пустой отзыв. Возможно вы говорили слишком тихо.'
    try:
        await rewiew_validator(text)
    except FeedbackError as e:
        answer = e.message
    if not answer:
        await save_review(text=text, state=state)
        answer = ms.SUCCESSFUL_MESSAGE
    await message.answer(text=answer)
    await state.set_state(Route.transition)


# Почему то надо нажать 2 раза да, чтобы перейти к следующему шагу
@route_router.message(Route.transition, F.voice | F.text)
async def transition(message: Message, state: FSMContext) -> None:
    '''Переход'''
    global target
    exhibit = await get_exhibit_from_state(state)
    while True:
        if message.text == 'Да':
            target = False
        if message.text != 'Да' and target:
            await message.answer(
                'Следующий объект расположен по адресу: '
                f'{exhibit.address}\n'
                'Получилось найти?\n'
                f'Возможно вам поможет: {exhibit.how_to_pass}',
                reply_markup=make_row_keyboard(['Да'])
            )
            await asyncio.sleep(3)
            continue

        break
    await state.set_state(Route.exhibit)


@route_router.message(Route.quiz)
async def end_route(message: Message, state: FSMContext) -> None:
    '''Конец маршрута'''
    await message.answer('Клманда будет рада отклику\nСсылка на форму')
    await state.clear()
    await message.answer(
        'Вернутся на выбор маршрута',
        reply_markup=make_row_keyboard(['/routes'])
    )


@route_router.message(F.text)
async def unknown_text(message: Message):
    """Ловит все сообщения от пользователя,
    если они не попадают под условиях функций выше.
    """
    await message.answer('Я тебя не понимаю, попробую использовать команды.')


@route_router.message(F.content_type.ANY)
async def unknown_message(message: Message):
    await message.reply(emoji.emojize(':astonished:', language='alias'),)
    message_text = text(
        'Я не знаю, что с этим делать ',
        italic('\nЯ просто напомню,'), 'что есть',
        code('команда'), '/help',
    )
    await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)
    await message.answer_dice('⚽')
    await message.answer_dice('🎰')
