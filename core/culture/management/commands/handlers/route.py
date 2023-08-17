import asyncio
import emoji

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


from ..config import logger, BASE_DIR
from ..functions import (
    get_id_from_state, speech_to_text_conversion,
    remove_tmp_files
)

from ..crud import (
    save_review, get_exhibit_by_id,
    get_route_by_name, get_all_exhibits_by_route,
    get_routes
)
from ..utils import Route
from ..keyboards import (
    make_row_keyboard, KEYBOARD_YES_NO
)
from .. import message as ms
from ..validators import feedback_validator
from ..exceptions import FeedbackError

route_router = Router()


@route_router.message(Command("routes"))
async def command_start(message: Message, state: FSMContext) -> None:
    """Команда /routes . Предлагает выбрать маршрут."""
    await message.reply(
        text=ms.CHOOSE_ROUTE_MESSAGE,
        reply_markup=make_row_keyboard(await get_routes()),
    )
    await state.set_state(Route.route)


@route_router.message(Route.route,  F.text == "Нет")
async def start_proute(message: Message, state: FSMContext) -> None:
    '''Поиск маршрута'''
    await message.answer('Медитация по адресу')
    await message.answer(
        'вы стоите в начале',
        reply_markup=make_row_keyboard(['да']),
        )


@route_router.message(Route.route,  F.text == 'Да')
async def start_path(message: Message, state: FSMContext) -> None:
    '''Старт медитации'''
    await state.update_data(exhibit_number=0)
    await message.answer(
        'Отлично начнем нашу медитацию',
        reply_markup=make_row_keyboard(['Отлично начинаем'])
    )
    await state.set_state(Route.exhibit)


@route_router.message(Route.route)
async def route_info(message: Message, state: FSMContext) -> None:
    """Начало пути """
    try:

        await get_route_by_name(message.text.capitalize())

    except ObjectDoesNotExist:
        logger.error('Пользователь ввел название маршрута, которого нет в бд.')
        await message.answer(
            'Выбери маршрут из тех, которые представлены на клавиатуре'
        )
        return
    await message.answer('Описания маршрута')
    await state.update_data(route=message.text.capitalize())
    await state.update_data(exhibit_number=0)
    await state.update_data(target=False)

    await message.answer(
        ms.START_ROUTE_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
    await state.set_state(Route.transition)


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

    route_name, exhibit_number = await get_id_from_state(state)
    exhibit = await get_exhibit_by_id(route_name, exhibit_number)
    await message.answer(
        f"Вы на марштруте  {route_name}"
        f" и экспонате {exhibit_number}"
        f"и описание {exhibit.description}",
    )
    image = FSInputFile(path='media/' + str(exhibit.image))
    await message.answer_document(image)
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
    data = await state.get_data()
    number_exhibit = data['exhibit_number'] + 1
    await state.update_data(exhibit_number=number_exhibit)
    route = await get_route_by_name(data['route'])
    if number_exhibit == len(await get_all_exhibits_by_route(route)):
        await message.answer(
            'Конец маршрута',
            reply_markup=make_row_keyboard(['Конец']),
        )
        await state.set_state(Route.quiz)
    else:
        await message.answer(
            'Нас ждут длительные переходы',
            reply_markup=make_row_keyboard(['Отлично идем дальше']),
        )
        await state.set_state(Route.transition)


@route_router.message(Route.transition, F.voice | F.text)
async def transition(message: Message, state: FSMContext) -> None:
    '''Переход'''

    data = await state.get_data()
    number_exhibit = data['exhibit_number']
    route = await get_route_by_name(data['route'])
    if message.text == 'Да' or message.text == 'Отлично идем дальше':
        if number_exhibit == 1:
            await message.answer(
                'Отлично начнем нашу медитацию',
            )
            await state.set_state(Route.exhibit)
            await exhibit(message, state)
        else:
            # # Картинка экспоната
            await message.answer(
                        'Следующий объект по адресу. Получилось найти',
                        reply_markup=make_row_keyboard(['Да'])
                )
            await asyncio.sleep(1)
            await state.set_state(Route.exhibit)
    elif message.text == 'Нет':
        await message.answer(
                'медитация начинается по адрусу\nВы стоите в начале маршрута',
                reply_markup=make_row_keyboard(['Да'])
        )
    else:
        if int(message.text) <= len(await get_all_exhibits_by_route(route)):
            await state.update_data(exhibit_number=int(message.text))
            await message.answer(
                    f'вы решили начать с экспоната {message.text}',
                    reply_markup=make_row_keyboard(['Да'])
            )
        else:
            await message.answer(
                    'Такого экспоната нету.'
                    'Введите номер экспоната или нажмите да'
                    'чтобы начать с начала пути',
                    reply_markup=make_row_keyboard(['Да'])
            )


@route_router.message(Route.quiz)
async def end_route(message: Message, state: FSMContext) -> None:
    '''Конец маршрута'''
    await message.answer('Клманда будет рада отклику\nСсылка на форму')
    await state.clear()
    await message.answer(
        'Вернутся на выбор маршрута',
        reply_markup=make_row_keyboard(['/routes'])
    )


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
    # Пока сделал через сохранение. Надо переделать на BytesIO
    answer = ''
    await message.bot.download(
        message.voice,
        destination=f'{BASE_DIR}/tmp/voices/{message.voice.file_id}.ogg'
    )
    try:
        text = await speech_to_text_conversion(filename=message.voice.file_id)
    except UnknownValueError:
        answer = 'Пустой отзыв. Возможно вы говорили слишком тихо.'
    try:
        await feedback_validator(text)
    except FeedbackError as e:
        answer = e.message
    if not answer:
        await save_review(text=text, state=state)
        await remove_tmp_files(filename=message.voice.file_id)
        answer = ms.SUCCESSFUL_MESSAGE
    await message.answer(text=answer)
    await state.set_state(Route.transition)


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
