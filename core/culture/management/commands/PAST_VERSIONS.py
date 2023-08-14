
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
