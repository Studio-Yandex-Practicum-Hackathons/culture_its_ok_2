import asyncio
import io
import random

from aiogram import Bot, F, Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (FSInputFile, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from django.core.exceptions import ObjectDoesNotExist
from speech_recognition.exceptions import RequestError, UnknownValueError

from .. import constants as const
from .. import message as ms
from ..config import MAXIMUM_DURATION_VOICE_MESSAGE, URL_TABLE_FEEDBACK, logger
from ..crud import (get_all_exhibits_by_route, get_exhibit, get_route_by_id,
                    get_routes_id, save_review, get_all_photos_by_exhibit)
from ..exceptions import FeedbackError
from ..functions import (get_exhibit_from_state, get_id_from_state,
                         get_route_from_state, get_tag_from_description,
                         set_route, speech_to_text_conversion, send_photo,)
from ..keyboards import (KEYBOARD_YES_NO, keyboard_for_send_review,
                         keyboard_for_transition, keyboard_yes,
                         make_row_keyboard, make_vertical_keyboard)
from ..utils import Block, Route
from ..validators import rewiew_validator

route_router = Router()


@route_router.message(Command("routes"))
@route_router.message(F.text == "Маршруты")
async def command_routes(message: Message, state: FSMContext) -> None:
    """Команда /routes . Предлагает выбрать маршрут."""
    keybord = []
    for route in await get_routes_id():
        keybord.append(const.ROUTE + str(route))
    if not keybord:
        await message.answer('На данный момент нет доступных маршрутов')
        return
    await message.reply(
         text=ms.CHOOSE_ROUTE_MESSAGE,
         reply_markup=make_vertical_keyboard(keybord),
    )
    await state.set_state(Route.choose)


@route_router.message(Route.route,  F.text.regexp(r"\d+"))
async def start_route_number(message: Message, state: FSMContext) -> None:
    """Поиск маршрута"""
    data = await state.get_data()
    count_exhibit = data.get("count_exhibits")
    if int(message.text) > count_exhibit:
        await message.answer(
            ms.ROUTE_SELECTION_ERROR.format(count_exhibit)
        )
        return
    number = int(message.text) - 1
    await state.update_data(exhibit_number=number)

    route_id, exhibit_number = await get_id_from_state(state)
    exhibit = await get_exhibit(route_id, exhibit_number)
    await state.update_data(exhibit=exhibit)

    await message.answer(
        ms.ADDRESS_SELECTED_OBJECT.format(message.text, exhibit.address),
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        ms.CHECK_PRESENCE,
        reply_markup=keyboard_yes(),
        )

    await state.set_state(Route.exhibit)


@route_router.message(Route.route,  F.text == const.NO)
async def start_route_no(message: Message, state: FSMContext) -> None:
    """Поиск маршрута"""
    route = await get_route_from_state(state)
    await message.answer(
        ms.ROUTE_MAP
    )
    image = FSInputFile(path=const.PATH_MEDIA + str(route.route_map))
    await send_photo(message, image)
    await message.answer(
        ms.CHECK_START_MEDITATION.format(route.address),
        reply_markup=keyboard_yes(),
    )


@route_router.message(Route.route,  F.text == const.YES)
async def start_route_yes(message: Message, state: FSMContext) -> None:
    """Старт медитации"""
    await message.answer(
        ms.START_MEDITATION,
        reply_markup=make_row_keyboard(["Отлично начинаем"])
    )
    exhibit = await get_exhibit_from_state(state)
    if exhibit.message_before_description != "":
        await message.answer(
            f"{exhibit.message_before_description}",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Route.podvodka)
    else:
        await state.update_data(
            answer_to_message_before_description=const.NOT_PODVODKA)
        await state.set_state(Route.exhibit)


@route_router.message(Route.route_start)
async def route_info_start(message: Message, state: FSMContext) -> None:
    """Информация о маршруте."""
    data = await state.get_data()
    route = data.get("route_obj")
    await message.answer(
        ms.EXHIBIT_SELECTION.format(route.address)
    )
    await message.answer(
        ms.START_ROUTE_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
    await state.set_state(Route.route)


@route_router.message(Route.choose)
async def route_info(message: Message, state: FSMContext, bot: Bot) -> None:
    """Начало пути """

    await state.set_state(Block.block)
    route_id = message.text.split(" ")[-1]
    try:
        route_id = int(route_id)
    except ValueError:
        await message.answer("Не получилось преобразовать в номер маршрута")
        await message.answer("Повторите попытку")
        await state.set_state(Route.choose)
        return
    try:
        route = await get_route_by_id(route_id)
    except ObjectDoesNotExist:
        logger.error("Пользователь ввел название маршрута, которого нет в бд.")
        await message.answer(
            ms.ROUTE_SELECTION_ERROR
        )
        return
    await message.answer(
        ms.ROUTE_DESCRIPTION.format(    
            route.name,
            route.description.replace('<p>', '').replace('</p>', '')
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(const.SLEEP_3)
    count_exhibits = len(await get_all_exhibits_by_route(route))
    await message.answer(
        ms.NUMBER_EXHIBITS_IN_ROUTE.format(count_exhibits)
    )

    image = FSInputFile(path=const.PATH_MEDIA + str(route.image))

    await send_photo(message, image)

    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    await asyncio.sleep(5)

    await message.answer(
        ms.ROUTE_MAP
    )

    image = FSInputFile(path=const.PATH_MEDIA + str(route.route_map))
    await send_photo(message, image)

    await state.update_data(route=route_id)
    await state.update_data(exhibit_number=0)
    await state.update_data(count_exhibits=count_exhibits)

    exhibit = await get_exhibit(route_id, 0)
    await state.update_data(route_obj=route)
    await state.update_data(exhibit=exhibit)

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(const.SLEEP_3)

    if route.text_route_start != "":
        await message.answer(
            f"{route.text_route_start.replace('<p>', '').replace('</p>', '')}",
            reply_markup=make_row_keyboard(["Хорошо"]),
        )
        await state.set_state(Route.route_start)
        return
    await message.answer(
        ms.EXHIBIT_SELECTION.format(route.address.replace('<p>', '').replace('</p>', ''))
    )
    await message.answer(
        ms.START_ROUTE_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
    await state.set_state(Route.route)


@route_router.message(Route.podvodka,)
async def podvodka(message: Message, state: FSMContext, bot: Bot) -> None:
    """Запись ответа подводки в state."""
    await state.update_data(
        answer_to_message_before_description=message.text)
    await exhibit_info(message, state, bot)


@route_router.message(Route.reflaksia,  F.text == const.NO)
async def refleksia_no(message: Message, state: FSMContext) -> None:
    """Отр рефлексия"""
    exhibit = await get_exhibit_from_state(state)
    await state.update_data(answer_to_reflection=message.text)
    if exhibit.reflection_negative != "":
        await message.answer(
            f"{exhibit.reflection_negative.replace('<p>', '').replace('</p>', '')}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "В бд нет отр рефлексии?",
        )
    await message.answer(
        ms.REVIEW_ASK,
        reply_markup=keyboard_for_send_review()
    )


# пока что только любой текст кроме слова нет
@route_router.message(Route.reflaksia,)
async def refleksia_yes(message: Message, state: FSMContext) -> None:
    """Положительная рефлексия"""
    exhibit = await get_exhibit_from_state(state)
    await state.update_data(answer_to_reflection=message.text)
    await message.answer(
        f"{exhibit.reflection_positive.replace('<p>', '').replace('</p>', '')}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        ms.REVIEW_ASK,
        reply_markup=keyboard_for_send_review()
    )


@route_router.message(
        Route.exhibit,
        F.text.in_(const.ANSWERS_TO_CONTINUE)
)
async def exhibit_info(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Отрпавляет сообщение с экспонатом,
    запускается если есть состояние Route.exhibit
    """
    await state.set_state(Block.block)

    # надо научится отправлять стикер пользователю (из набора рандомный)

    # await message.reply(emoji.emojize(":thumbs_up:", language="alias"),)
    await message.reply(random.choice(ms.EMOJI_LIST))

    exhibit = await get_exhibit_from_state(state)

    await message.answer(
        await get_tag_from_description(exhibit.description),
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    await asyncio.sleep(const.SLEEP_3)
    photos = await get_all_photos_by_exhibit(exhibit)
    for photo in photos:
        image = FSInputFile(path=const.PATH_MEDIA + str(photo.image))
        await send_photo(message, image)

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(const.SLEEP_10)

    if exhibit.reflection != "":
        await message.answer(
            f"{exhibit.reflection.replace('<p>', '').replace('</p>', '')}",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=KEYBOARD_YES_NO,
                resize_keyboard=True,
            )
        )
        await state.set_state(Route.reflaksia)
    else:
        await state.update_data(answer_to_reflection=const.NOT_REFLAKSIA)
        await message.answer(
            ms.REVIEW_ASK,
            reply_markup=keyboard_for_send_review()
        )


@route_router.message(Route.review, F.text | F.voice)
async def review(message: Message, state: FSMContext) -> None:
    """Получения отзыва"""
    answer = ""
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
                answer = ms.EMPTY_REVIEW
            except RequestError:
                answer = ms.USE_TEXT_REVIEW
        else:
            answer = ms.SHORT_VOICE_REVIEW.format(
                MAXIMUM_DURATION_VOICE_MESSAGE
            )
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
        await message.answer(
            text=answer,
            reply_markup=make_row_keyboard(["Отлично идем дальше"]),
        )
        await set_route(state, message)
    else:
        await message.answer(text=ms.REVIEW_ERROR.format(answer),
                             reply_markup=keyboard_for_send_review())


@route_router.callback_query(F.data == "send_review")
async def resend_review(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup()
    await callback.message.answer(ms.WRITE_YOUR_OPINION)
    await state.set_state(Route.review)


@route_router.callback_query(F.data == "dont_send_review")
async def skip_send_review(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        'Очень жаль 😕',
        reply_markup=make_row_keyboard(["Идем дальше"]),
    )
    await set_route(state, callback.message)


@route_router.callback_query(Route.transition, F.data == "in_place")
async def in_place(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    """Кнопка "На месте", переход на некст объект."""
    await callback.answer()
    await callback.message.edit_reply_markup()
    exhibit_obj = await get_exhibit_from_state(state)
    if exhibit_obj.message_before_description != "":
        await callback.message.answer(
            f"{exhibit_obj.message_before_description.replace('<p>', '').replace('</p>', '')}",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Route.podvodka)
    else:
        await state.update_data(
            answer_to_message_before_description=const.NOT_PODVODKA)
        await exhibit_info(callback.message, state, bot)


@route_router.callback_query(Route.transition, F.data == "route")
async def show_route(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Кнопка "Маршрут", что-то делает ?."""
    await callback.answer()
    data = await state.get_data()
    route = data.get("route_obj")
    image = FSInputFile(path=const.PATH_MEDIA + str(route.route_map))
    await callback.message.answer(
        "Вот карта маршрута, надеюсь она вам поможет"
    )
    await send_photo(callback.message, image)


@route_router.message(Route.transition, F.text)
async def transition(message: Message, state: FSMContext) -> None:
    """Переход на следющий объект"""
    exhibit_obj = await get_exhibit_from_state(state)
    await message.answer(
        ms.INFO_NEXT_OBJECT.format(
            exhibit_obj.address.replace('<p>', '').replace('</p>', ''),
            exhibit_obj.how_to_pass.replace('<p>', '').replace('</p>', '')
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="Когда будешь на месте сообщи мне",
        reply_markup=keyboard_for_transition())


@route_router.message(Route.quiz,  F.text == "Да")
async def return_route(message: Message, state: FSMContext) -> None:
    """Вернутся на марщрут"""
    await state.set_state(None)
    await command_routes(message, state)


@route_router.message(Route.quiz,  F.text == "Нет")
async def leave_route(message: Message, state: FSMContext) -> None:
    """Уход с маршрута"""
    await message.answer(
        "Команда фестиваля прощается с Вами! Всего наилучшего!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@route_router.message(Route.quiz, F.text == "Конец")
async def end_route(message: Message, state: FSMContext) -> None:
    """Конец маршрута"""
    await message.answer(ms.RESPONSE_MESSAGE.format(URL_TABLE_FEEDBACK))
    await message.answer(
        ms.RETURN_TO_ROUTES,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,
        )
    )
