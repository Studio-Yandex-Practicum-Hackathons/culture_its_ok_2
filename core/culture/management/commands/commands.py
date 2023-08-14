"""Основные команды бота. Кнопки старт и маршруты"""
import emoji

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, ReplyKeyboardMarkup,
    ReplyKeyboardRemove, FSInputFile
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import text, italic, code
from django.core.exceptions import ObjectDoesNotExist
from speech_recognition.exceptions import UnknownValueError

from .functions import (
    get_id_from_state, speech_to_text_conversion,
    add_user_information,
)
from .crud import (
    feedback, get_exhibit_by_id,
    get_route_by_name, get_all_exhibits_by_route,
    get_routes, get_number_routes
)
from .utils import Route, User
from .keyboards import (
    make_row_keyboard, KEYBOARD_YES_NO, REVIEW_KEYBOARD,
    KEYBOARD_START, make_vertical_keyboard
)
from .message import (
    GREETING_MESSAGE, CHOOSE_ROUTE, SUCCESSFUL_MESSAGE, hello, age, hobby
)
from .validators import (check_name, check_age, feedback_validator)
from .exceptions import FeedbackError

form_router = Router()

available_routes = [f'Маршрут {i+1}'for i in range(get_number_routes())]
main_batten = ["/СТАРТ", 'Знакомство', 'help']


@form_router.message(CommandStart())
async def command_main_start(message: Message) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        hello,
        reply_markup=make_vertical_keyboard(main_batten)
    )


@form_router.message(F.text == "Знакомство")
async def get_acquainted(message: Message, state: FSMContext) -> None:
    '''Знакомство'''
    await message.answer("Давай познакомимся.\nКак тебя зовут?")
    await state.set_state(User.name)


@form_router.message(User.name)
async def get_name(message: Message, state: FSMContext) -> None:
    """Получает имя пользователя"""
    if await check_name(message.text):
        await state.update_data(name=message.text)
        await message.answer(age)
        await state.set_state(User.age)
    else:
        await message.answer('Некорректное имя. Еше раз')
        await state.set_state(User.name)


@form_router.message(User.age)
async def get_age(message: Message, state: FSMContext) -> None:
    """Получает возраст пользователя"""
    if await check_age(message.text):
        await state.update_data(age=message.text)
        await message.answer(hobby)
        await state.set_state(User.hobby)
    else:
        await message.answer('Некорректный возраст')
        await message.answer(age)


@form_router.message(User.hobby)
async def get_hobby(message: Message, state: FSMContext) -> None:
    """Получает хобби пользователя"""
    await state.update_data(hobby=message.text)
    await add_user_information(state)
    await message.answer(
        'Приятно познакомится',
        reply_markup=make_vertical_keyboard(main_batten)
    )
    await state.clear()


@form_router.message(Command("СТАРТ"))
async def command_start(message: Message, state: FSMContext) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        text=GREETING_MESSAGE
    )
    await message.reply(
        text=CHOOSE_ROUTE,
        reply_markup=make_row_keyboard(await get_routes()),
    )
    await state.set_state(Route.route)


@form_router.message(Command(commands=["cancel"]))
@form_router.message(F.text.casefold() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


# @form_router.message(Route.route, F.text)
# async def route(message: Message, state: FSMContext) -> None:
#     """Отрпавляет сообщение с выбранным маршрутом,
#     запускается если есть состояние Route.route.
#     Чек лист 4.2.1
#     """
#     await state.update_data(route=message.text.lower())
#     user_data = await state.get_data()
#     try:
#         route = await get_route_by_name(user_data['route'])
#     except ObjectDoesNotExist:
#         await message.answer(
#             'Выбери маршрут из тех, которые представлены на клавиатуре'
#         )
#         return
#     exhibits = await get_all_exhibits_by_route(route)
#     await message.answer(
#         f"Вы выбрали марщтур  {route.id} {route.name} {route.description}"
#         f"количество экспонатов {len(exhibits)}",
#     )
#     await asyncio.sleep(1)
#     await state.set_state(Route.exhibit)
#     await exhibit_first(message, state)


# # закомментил так как сама функция не должна вызываться пользователем
# # она вызывается только при выборе маршрута
# # так же можно добавить условие если пользватель воддит число, то
# # это число будет номер экспоната
# # @form_router.message(Route.exhibit, F.text)
# async def exhibit_first(message: Message, state: FSMContext) -> None:
#     """
#     Отрпавляет сообщение о начале марштура, запускается если
#     есть состояние Route.exhibit.
#     В чек листе 4.1.
#     """
#     await state.update_data(exhibit=0)
#     route_id, exhibit_id = await get_id_from_state(state)
#     await message.answer(
#         f"Вы на марштруте  {route_id}"
#         f"Вы стоите в точке начала маршрута?)",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=KEYBOARD_YES_NO,
#             resize_keyboard=True,
#         ),
#     )


@form_router.message(Route.route,  F.text == "No")
async def start_proute(message: Message, state: FSMContext) -> None:
    '''Поиск маршрута'''
    await message.answer('Медитация по адресу')
    await message.answer(
        'вы стоите в начале',
        reply_markup=make_row_keyboard(['да']),
        )


@form_router.message(Route.route,  F.text == 'Yes')
async def start_path(message: Message, state: FSMContext) -> None:
    '''Старт медитации'''
    await state.update_data(exhibit_number=1)
    await message.answer(
        'Отлично начнем нашу медитацию',
        reply_markup=make_row_keyboard(['Отлично начинаем'])
    )
    await state.set_state(Route.exhibit)


@form_router.message(Route.route)
async def route_info(message: Message, state: FSMContext) -> None:
    """Начало пути """
    await message.answer('Описания маршрута')
    await state.update_data(route=message.text.lower())
    try:
        await get_route_by_name(message.text.lower())
    except ObjectDoesNotExist:
        await message.answer(
            'Выбери маршрут из тех, которые представлены на клавиатуре'
        )
    return
    # await state.update_data(route=get_route_index(message.text))
    await message.answer(
        'начало',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )


# @form_router.message(Route.exhibit)
# async def exhibit_information(message: Message, state: FSMContext) -> None:
#     '''Обзор экспонат'''
#     data = await state.get_data()
#     await message.answer(
#         f'Про экспонат {data["route"]["exhibits"]
#           [data["exhibit_number"]-1][1]}'
#     )
#     await message.answer(
#         'о чем думаете Опишите',
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await state.set_state(Route.review)


@form_router.message(
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
    # Должна быть проверка что следующий экспонат сущетсвует,
    # если нет то это конец и надо вызвать другую функцию

    route_name, exhibit_number = await get_id_from_state(state)
    exhibit = await get_exhibit_by_id(route_name, exhibit_number)
    await message.answer(
        f"Вы на марштруте  {route_name}"
        f" и экспонате {exhibit_number}"
        f"и описание {exhibit.description}",
    )
    image = FSInputFile(path='media/' + str(exhibit.image))
    await message.answer_photo(image)
    await message.answer(
        'Заполни отзыв на экспонат или что думаете?(фитч лист)',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Route.review)


@form_router.message(Route.review, F.voice | F.text)
async def review(message: Message, state: FSMContext) -> None:
    '''Получения отзыва'''
    if message.voice:
        text = await feedback_validator(
            speech_to_text_conversion(message.voice)
        )
    elif message.text:
        # text = await feedback_validator(message.text)
        text = message.text
    await feedback(text, state)
    await message.answer('Спасибо за ваше наюддение')
    data = await state.get_data()
    number_exhibit = data['exhibit_number'] + 1
    await state.update_data(exhibit_number=number_exhibit)
    route = await get_route_by_name(data['route'])
    if data['exhibit_number'] >= len(await get_all_exhibits_by_route(route)):
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


@form_router.message(Route.transition)
async def transition(message: Message, state: FSMContext) -> None:
    '''Переход'''
    await message.answer(
        'Следующий объект по адресу. Получилось найти',
        reply_markup=make_row_keyboard(['Да'])
    )
    # Картинка экспоната
    await state.set_state(Route.exhibit)


@form_router.message(Route.quiz)
async def end_route(message: Message, state: FSMContext) -> None:
    '''Конец маршрута'''
    await message.answer('Клманда будет рада отклику\nСсылка на форму')
    await state.clear()
    await message.answer(
        'Вернутся на выбор маршрута',
        reply_markup=make_row_keyboard(['/СТАРТ'])
    )


@form_router.message(F.text == "help")
async def help_info(message: Message) -> None:
    await message.answer('Тут описаны подсказки')


# @form_router.message(Route.review, F.text)
# async def review(message: Message, state: FSMContext) -> None:
#     """Запускается если есть состояние Route.review.
#     Чек лист 4.5 - 4.7.2.
#     В конце должен вызвать функцию, которая выводит следующий экспонат.
#     На данный момент это exhibit_yes и exhibit_no.
#     """
#     await message.answer(f'ваш отзыв - {message.text}')
#     await feedback(message.text, state)
#     user_data = await state.get_data()
#     number_exhibit = user_data['exhibit']
#     route = await get_route_by_name(user_data['route'])
#     if number_exhibit == len(await get_all_exhibits_by_route(route)):
#         await message.answer(
#             'Это конец, пройди опрос',
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.set_state(Route.quiz)
#         return

#     await message.answer(text=SUCCESSFUL_MESSAGE)
#     await message.answer(
#         'Спасибо за наблюдения \n Перейти к следующему экспонату?',
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=REVIEW_KEYBOARD,
#             resize_keyboard=True,
#         ),
#     )
#     await message.answer('Получилось ли найти объект(4.7.2?)')
#     await state.set_state(Route.exhibit)


# @form_router.message(Route.quiz)
# async def quiz(message: Message, state: FSMContext) -> None:
#     """Отрпавляет сообщение с просьбой пройти опрос, запускается если
#     есть состояние Route.quiz.
#     Чек лист 7-8.1.1.
#     В конце должен вызвать функцию, которая выводит активные марштруты.
#     (На данный момент это кнопка start, но кнопка старт
#     должна только приветствовать пользователя в начале)
#     """
#     await message.answer('Спасибо за опрос.')
#     await message.answer(
#         text="Выбери марштур",
#         reply_markup=make_row_keyboard(await get_routes()),
#     )
#     await state.set_state(Route.route)


# @form_router.message(Route.exhibit,  F.text.casefold() == "no")
# async def exhibit_no(message: Message, state: FSMContext) -> None:
#     """
#     Отрпавляет сообщение если пользователь
#     нажал на кнопку нет, при активном Route.exhibit.
#     Должен вывести карту (смотри чек лист 4.3.1 - 4.3.2)
#     Так же должен вызывать функцию ( чек лист 4.4)
#     """
#     user_data = await state.get_data()
#     await message.reply(
#         f"Выбрано НЕТ .... Вы ушли с марштура {user_data['route']} "
#         "При нажатии на кнопку появляются текстовые сообщения"
#         "и ссылка на Яндекс.карты. ",
#     )
#     await message.answer(
#         text="Выбери марштур",
#         reply_markup=make_row_keyboard(await get_routes()),
#     )
#     await message.answer(
#         f'{user_data}'
#     )
#     await state.set_state(Route.route)


@form_router.message(F.voice)
async def get_voice_review(message: Message, state: FSMContext, bot: Bot):
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
    await bot.download(
        message.voice,
        destination=f'/tmp/{message.voice.file_id}.ogg'
    )
    try:
        text = await speech_to_text_conversion(
            filename=message.voice.file_id, message=message
        )
    except UnknownValueError:
        answer = 'Пустой отзыв. Возможно вы говорили слишком тихо.'
    try:
        await feedback_validator(text)
    except FeedbackError as e:
        answer = e.message
    if not answer:
        await feedback(text=text, user=message.from_user)
        answer = SUCCESSFUL_MESSAGE
    await message.answer(text=answer)


@form_router.message(F.text)
async def unknown_text(message: Message):
    """Ловит все сообщения от пользователя,
    если они не попадают под условиях функций выше.
    """
    await message.answer('Я тебя не понимаю, попробую использовать команды.')


@form_router.message(F.content_type.ANY)
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
