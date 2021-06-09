from django.core.exceptions import ObjectDoesNotExist
from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from accounts.models import Organization, Users

DEEP_LINK = '/start '
ORGANIZATION_ID = ''
@processor(state_manager, from_states=state_types.All, success='is_deep_link', fail='not_deep_link')
def hello_level_1(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        if (DEEP_LINK in update.message.text) and len(update.message.text) > 40:
            ORGANIZATION_ID = parse_message_text(update.message.text)
            org = is_organization(ORGANIZATION_ID)
            new_user = Users.objects.get_or_create(tg_user=state.telegram_user, organization_id=org, username=state.telegram_user.username)
            bot.sendMessage(update.get_chat().get_id(), f'Добро пожаловать к боту! Мы успешно сохранили данные о Вас, {state.telegram_user.username}, но перед тем, как пойти дальше, Вы должны указать Ваше имя следующим сообщением. Оно будет использоваться для подписи контейнеров с Вашей заказанной едой. В будущем Вы в любой момент сможете его изменить.')
            raise ProcessFailure
        else:
            bot.sendMessage(update.get_chat().get_id(), f'Привет, {state.telegram_user.username}! ')

    except AttributeError:
        pass

@processor(state_manager, from_states='not_deep_link')
def hello_level_2(bot, update, state):
    new_user = Users.objects.get(tg_user=state.telegram_user)
    new_user.username = update.message.text
    new_user.save()

# Дополнительные методы для последующмх задач

# @processor(state_manager, from_states='is_deep_link', success='is_user', fail='not_user')
# def hello_level_3(bot, update, state):
#     if not is_user(state.telegram_user):
#         raise ProcessFailure

# @processor(state_manager, from_states='is_user')
# def hello_level_4(bot, update, state):
#     bot.sendMessage(update.get_chat().get_id(), f'Ты {state.telegram_user.username}')
#
# @processor(state_manager, from_states='not_user', success='to_sign_up')
# def hello_level_5(bot, update, state):
#     bot.sendMessage(update.get_chat().get_id(), f'{state.telegram_user.username}, нужна регистрация! отправь имя ')

#
# @processor(state_manager, from_states='to_sign_up')
# def hello_level_5(bot, update, state):
#     new_user = Users()
#     new_user.username = update.message.text
#     new_user.tg_user = state.telegram_user
#     new_user.organization_id = is_organization(ORGANIZATION_ID)
#     new_user.save()

    # second_key = parse_message_text(update.message.text)
    # print(update.message.text)
    # organization = is_organization(second_key)
    # bot.sendMessage(update.get_chat().get_id(), f'Рады видеть Вас, {state.telegram_user.username}')


def is_organization(second_key):
    try:
        return Organization.objects.get(secondary_key=second_key)
    except ObjectDoesNotExist:
        return False

def is_user(user_id):
    try:
        return Users.objects.get(tg_user=user_id)
    except ObjectDoesNotExist:
        return False

def parse_message_text(message_text):
    return message_text.split(' ')[-1]


