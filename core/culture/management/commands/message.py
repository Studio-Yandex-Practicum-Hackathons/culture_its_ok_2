"""Файл с основными ответами бота. Должны быть основные шаблоны ответов."""

SUCCESSFUL_MESSAGE: str = 'Спасибо за отзыв.'

GREETING_MESSAGE = (
    'Добрый день!'
    'Вас Приветствует официальный бот арт-медиатор проекта'
    '"Ничего страшного"'
)
INTRODUCTORY_MESSAGE = 'Давай познакомимся. Как тебя зовут'
AGE_MESSAGE = 'Укажите свой возраст'
HOBBY_MESSAGE = ('Может быть у вас есть хобби?\n'
                 'Выберете из списка, '
                 'если вашего хобби нет в списке нажмите другое')
CHOOSE_ROUTE_MESSAGE = (
    'Выбери маршурт из предложенных'
)
MAP_INFORMATION_MESSAGE = (
    'Перед Вами карта фестиваля.'
    'Фестиваль в этом году объединяет 100 работ.'
    'Мы разработали столько маршрутов'
)
START_ROUTE_MESSAGE = 'Или Вы стоите в начале маршрута?'
REVIEW_ASK = 'Вам понравилось? Напишите, пожалуйста, свои впечатления.'
NAME_ERROR = 'Некорректное имя. Еше раз'
AGE_ERROR = 'Некорректный возраст'
END_ACQUAINTANCE = '''
Приятно познакомится {}!
Нажмите на команду /routes для выбора маршрута.
'''
ROUTE_SELECTION_ERROR = '''
Вы ввели число, которое превышает {}
Пожалуйста повторите попытку или выберете Да/Нет
'''
ADDRESS_SELECTED_OBJECT = '''
Вы выбрали номер объекта={}
Обьект расположен по адресу: {}
'''
CHECK_PRESENCE = 'Нажмите Да, когда будете возле экспоната'
CHECH_NEXT_PRESENCE = 'Нажмите Да, когда дойдете до следущего экспонат.'
CHECK_START_MEDITATION = '''
Медитация начинается по адресу {}
Вы стоите в начале?
'''
START_MEDITATION = 'Отлично начнем нашу медитацию'
ROUTE_SELECTION_ERROR = ('Выбери маршрут из тех, '
                         'которые представлены на клавиатуре')
ROUTE_DESCRIPTION = '''
Название маршрута: {}
{}\n
'''
NUMBER_EXHIBITS_IN_ROUTE = 'Данный маршрут состоит из {} экспонатов!'
ROUTE_COVER = 'Обложка маршрута !'
ROUTE_MAP = 'Карта маршрута !'
EXHIBIT_SELECTION = '''
Медитация начинается по адресу: {}
Если хотите выбрать номер обекта напишите его номер
'''
REVIEW_ERROR = '{}\nПопробуйте снова.'
WRITE_YOUR_OPINION = 'Напишите ваше мнение'
INFO_NEXT_OBJECT = '''
Следующий объект расположен по адресу:
{}
Как добраться: {}
'''
RESPONSE_MESSAGE = 'Команда будет рада отклику\nСсылка на форму'
RETURN_TO_ROUTES = 'Вернутся на выбор маршрута'
EMPTY_REVIEW = 'Пустой отзыв. Возможно вы говорили слишком тихо.'
USE_TEXT_REVIEW = '''
В данный момент я не могу понимать голосовые
сообщения. Используй, пожалуйста, текст.
'''
SHORT_VOICE_REVIEW = 'Голосовое сообщение должно быть менее {}'
