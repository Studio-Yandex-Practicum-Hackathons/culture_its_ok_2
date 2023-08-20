import asyncio

import emoji
import io

from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (FSInputFile, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.markdown import code, italic, text
from django.core.exceptions import ObjectDoesNotExist
from speech_recognition.exceptions import RequestError, UnknownValueError


from .. import message as ms
from ..config import logger, MAXIMUM_DURATION_VOICE_MESSAGE
from ..crud import (get_all_exhibits_by_route, get_exhibit, get_route_by_id,
                    get_routes_id, save_review)
from ..exceptions import FeedbackError
from ..functions import (get_exhibit_from_state, get_id_from_state,
                         get_route_from_state,
                         speech_to_text_conversion)
from ..keyboards import (KEYBOARD_YES_NO, make_row_keyboard,
                         make_vertical_keyboard)
from ..utils import Route, Block
from ..validators import rewiew_validator

route_router = Router()

target = True


@route_router.message(Command("routes"))
async def command_start(message: Message, state: FSMContext) -> None:
    """Команда /routes . Предлагает выбрать маршрут."""
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
    data = await state.get_data()
    count_exhibit = data.get('count_exhibits')
    if int(message.text) > count_exhibit:
        await message.answer(
            f'Вы ввели число, которое превышает {count_exhibit} \n'
            f'Пожалуйста повторите попытку или выберет Да/Нет'
        )
        return
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
    await state.update_data(exhibit_obj=exhibit)
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
    exhibit = await get_exhibit_from_state(state)
    if exhibit.message_before_description != '':
        await message.answer(
            f"{exhibit.message_before_description}",
        )
        await state.set_state(Route.podvodka)
    else:
        await state.update_data(podvodka=None)
        await state.set_state(Route.exhibit)


@route_router.message(Route.route)
async def route_info(message: Message, state: FSMContext) -> None:
    """Начало пути """

    await state.set_state(Block.block)
    route_id = message.text.split(' ')[-1]
    try:
        route = await get_route_by_id(route_id)
    except ObjectDoesNotExist:
        logger.error('Пользователь ввел название маршрута, которого нет в бд.')
        await message.answer(
            'Выбери маршрут из тех, которые представлены на клавиатуре'
        )
        return
    await message.answer(
        f"Название маршрута: {route.name}\n"
        f"{route.description}\n"
    )
    await asyncio.sleep(3)
    count_exhibits = len(await get_all_exhibits_by_route(route))
    await message.answer(
        f'Данный маршрут состоит из {count_exhibits} экспонатов!'
    )

    await message.answer(
        'Обложка маршрута !'
    )
    image = FSInputFile(path='media/' + str(route.image))
    await message.answer_photo(image)

    await asyncio.sleep(3)

    await message.answer(
        'Карта маршрута !'
    )
    image = FSInputFile(path='media/' + str(route.route_map))
    await message.answer_photo(image)

    await state.update_data(route=route_id)
    await state.update_data(exhibit_number=0)
    await state.update_data(count_exhibits=count_exhibits)

    exhibit = await get_exhibit(route_id, 0)
    await state.update_data(route_obj=route)
    await state.update_data(exhibit_obj=exhibit)

    await message.answer(
        ms.START_ROUTE_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
    await message.answer('Если хотите выбрать номер обекта напишите его номер')
    await state.set_state(Route.route)


@route_router.message(Route.podvodka,)
async def podvodka(message: Message, state: FSMContext) -> None:
    await state.update_data(podvodka=message.text)
    await exhibit(message, state)


@route_router.message(Route.reflaksia,  F.text == 'Нет')
async def refleksia_no(message: Message, state: FSMContext) -> None:
    '''Отр рефлексия'''
    # exhibit = await get_exhibit_from_state(state)
    await state.update_data(refleksia=message.text)
    await message.answer(
        "ТУТ ОТР РЕФЛЕКСИЯ",
    )
    await message.answer(
        'Вам понравилось? напишите, пожалуйста, свои впечатления.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Route.review)


# пока что только любой текст кроме слова нет
@route_router.message(Route.reflaksia,)
async def refleksia_yes(message: Message, state: FSMContext) -> None:
    '''Положительная рефлексия'''
    exhibit = await get_exhibit_from_state(state)
    await state.update_data(refleksia=message.text)
    await message.answer(
        f"{exhibit.reflection_positive}",
    )
    await message.answer(
        'Вам понравилось? напишите, пожалуйста, свои впечатления.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Route.review)


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
    await state.set_state(Block.block)

    # надо научится отправлять стикер пользователю (из набора рандомный)

    await message.reply(emoji.emojize(':thumbs_up:', language='alias'),)

    exhibit = await get_exhibit_from_state(state)

    await message.answer(
        f"{exhibit.description}",
    )

    image = FSInputFile(path='media/' + str(exhibit.image))
    await message.answer_photo(image)

    await asyncio.sleep(10)

    if exhibit.reflection != '':
        await message.answer(
            f"{exhibit.reflection}",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=KEYBOARD_YES_NO,
                resize_keyboard=True,
            )
        )
        await state.set_state(Route.reflaksia)
    else:
        await message.answer(
            'Вам понравилось? напишите, пожалуйста, свои впечатления.',
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Route.review)


def keyboard_for_send_review():
    buttons = [
        [
            types.InlineKeyboardButton(
                text='Оставить отзыв', callback_data='send_review'
            ),
            types.InlineKeyboardButton(
                text='Без отзыва', callback_data='dont_send_review'
            )
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@route_router.message(Route.review, F.text | F.voice)
async def review(message: Message, state: FSMContext) -> None:
    '''Получения отзыва'''
    global target
    target = True
    print(await state.get_data())
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text='Оставить отзыв',
    #     callback_data='send_review'
    # ))
    answer = ''
    if message.voice:
        if message.voice.duration <= MAXIMUM_DURATION_VOICE_MESSAGE:
            voice_file = io.BytesIO()
            await message.bot.download(
                message.voice,
                destination=voice_file
            )
            try:
                text = await speech_to_text_conversion(filename=voice_file)
            except UnknownValueError:
                answer = 'Пустой отзыв. Возможно вы говорили слишком тихо.'
            except RequestError:
                answer = ('В данный момент я не могу понимать голосовые '
                          'сообщения. Используй, пожалуйста, текст.')
        else:
            answer = (f'Голосовое сообщение должно быть менее '
                      f'{MAXIMUM_DURATION_VOICE_MESSAGE}')
    else:
        text = message.text
    if not answer:
        try:
            await rewiew_validator(text)
        except FeedbackError as e:
            answer = e.message

    if not answer:
        await save_review(text, state)
        answer = ms.SUCCESSFUL_MESSAGE
        await message.answer(text=answer)

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
            await state.update_data(exhibit_obj=exhibit)
            await state.set_state(Route.transition)
    else:
        await message.answer(text=f'{answer}\nПопробуйте снова.',
                             reply_markup=keyboard_for_send_review())
        # await state.set_state(Route.review)


@route_router.callback_query(F.data == 'send_review')
async def resend_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Напишите ваше мнение')
    await state.set_state(Route.review)


@route_router.callback_query(F.data == 'dont_send_review')
async def skip_send_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    exhibit = await get_exhibit_from_state(state)

    route_id, exhibit_number = await get_id_from_state(state)
    exhibit_number += 1
    await state.update_data(exhibit_number=exhibit_number)
    route = await get_route_by_id(route_id)
    if exhibit_number == len(await get_all_exhibits_by_route(route)):
        await callback.message.answer(
            'Конец маршрута',
            reply_markup=make_row_keyboard(['Конец']),
        )
        await state.set_state(Route.quiz)
    else:
        if exhibit.transfer_message != '':
            await callback.message.answer(
                f"{exhibit.transfer_message}",
            )
        await callback.message.answer(
            'Нас ждут длительные переходы',
            reply_markup=make_row_keyboard(['Отлично идем дальше']),
        )
        exhibit = await get_exhibit(route_id, exhibit_number)
        await state.update_data(exhibit_obj=exhibit)
        await state.set_state(Route.transition)


# этот код будет работать только если ботом пользуется только один человек,
# надо как-то связать target c активным пользовелем
@route_router.message(Route.transition, F.text)
async def transition(message: Message, state: FSMContext) -> None:
    '''Переход'''
    global target
    exhibit_obj = await get_exhibit_from_state(state)
    while True:
        if not target:
            break
        if message.text == 'Да' and target:
            target = False
            if exhibit_obj.message_before_description != '':
                await message.answer(
                    f"{exhibit_obj.message_before_description}",
                )
                # не много не так работает , но работает
                await state.set_state(Route.podvodka)
            else:
                await state.update_data(podvodka=None)
                await exhibit(message, state)
            break
        if message.text != 'Да' and target:
            await message.answer(
                        'Следующий объект расположен по адресу: '
                        f'{exhibit_obj.address}\n'
                        'Получилось найти?\n'
                        f'Возможно вам поможет: {exhibit_obj.how_to_pass}',
                        reply_markup=make_row_keyboard(['Да'])
                    )
            await asyncio.sleep(3)
            continue


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
