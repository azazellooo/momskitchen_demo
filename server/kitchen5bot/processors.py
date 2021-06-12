from django.core.exceptions import ObjectDoesNotExist
from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from accounts.models import Organization, Users
from .parse_and_validations import deep_link_parce, is_organization, is_user, deep_len_validator

DEEP_LINK = '/start '
STOP = '/stop'
START = '/start'
ORGANIZATION_ID = None

# Задаем декоратору fail=state_types.Keep который будет выполнять операцию возврата на исходное положение процессора то есть в саоме начало, затем добавляем методы
# raise ProcessFailure где нам нужно возвращать исходное положение процессора, затем я добавил ветвление elif state.name != 'iv, которое отвечает на любое сообщение, почему state.name != 'iv?
# потому что в базе сохраняется state.name пока мы его не удалим командой state.set_name(''), а как раз таки мы это делаем в процессоре 'iv' который апдейтит юзернейм для контейнеров
# и при первой итерации когда он попадает в success то есть в наш 'iv', то он одновременно с name который лежит в базе так как мы казали success='iv', запускал наше ветвление else так как это не токен.
# надеюсь обьяснил понятно....

@processor(state_manager,  from_states=state_types.All, update_types=update_types.Message, message_types=message_types.Text, success='iv', fail=state_types.Keep)
def hello_level_1(bot: TelegramBot, update: Update, state: TelegramState):
    state.reset_memory()
    if DEEP_LINK in update.message.text and deep_len_validator(update.message.text):
        ORGANIZATION_ID = deep_link_parce(update.message.text)
        org = is_organization(ORGANIZATION_ID)
        if org is not None:
            if Users.objects.filter(tg_user=state.telegram_user, organization_id=org).exists():
                bot.sendMessage(update.get_chat().get_id(), f'Ты уже переходил мать его, {state.telegram_user.username}!')
                raise ProcessFailure
            else:
                Users.objects.create(
                    tg_user=state.telegram_user,
                    organization_id=org
                )
                bot.sendMessage(update.get_chat().get_id(), f'Добро пожаловать к боту! Мы успешно сохранили данные о Вас, {state.telegram_user.username}, но перед тем, как пойти дальше, Вы должны указать Ваше имя следующим сообщением. Оно будет использоваться для подписи контейнеров с Вашей заказанной едой. В будущем Вы в любой момент сможете его изменить.')
                return
        else:
            bot.sendMessage(update.get_chat().get_id(), 'Прекрасно подделываешь токен, научи так же')
            bot.sendMessage(update.get_chat().get_id(), f'Не пиши сюда больше, {state.telegram_user.username}! ')
            raise ProcessFailure
    elif update.message.text == STOP:
        try:
            the_user = Users.objects.get(tg_user=state.telegram_user)
            if the_user.is_active == True:
                the_user.is_active = False
                the_user.save()
                bot.sendMessage(update.get_chat().get_id(), 'Рассылка отключена.')
                raise ProcessFailure
            else:
                bot.sendMessage(update.get_chat().get_id(), 'Рассылка уже отключена.')
                raise ProcessFailure
        except ObjectDoesNotExist:
            bot.sendMessage(update.get_chat().get_id(), 'К сожалению мы не смогли найти ваш аккаунт. Пройдите регистрацию перейдя по ссылке, которую даст вам Никита.')
            raise ProcessFailure
    elif update.message.text == START:
        try:
            the_user = Users.objects.get(tg_user=state.telegram_user)
            if the_user.is_active == False:
                the_user.is_active = True
                the_user.save()
                bot.sendMessage(update.get_chat().get_id(), f'Привет, {state.telegram_user.username}! Рады видеть Вас снова в KitchenBot!')
                raise ProcessFailure
            else:
                bot.sendMessage(update.get_chat().get_id(), 'Рассылка уже включена.')
                raise ProcessFailure
        except ObjectDoesNotExist:
            bot.sendMessage(update.get_chat().get_id(), 'К сожалению мы не смогли найти ваш аккаунт. Пройдите регистрацию перейдя по ссылке, которую даст вам Никита.')
            raise ProcessFailure
    elif state.name != 'iv':
        bot.sendMessage(update.get_chat().get_id(), f'Здарова, {state.telegram_user.username}! ')
        raise ProcessFailure



@processor(state_manager, from_states='iv')
def hello_level_2(bot, update, state):
    user = Users.objects.get(tg_user=state.telegram_user)
    user.username = update.message.text
    user.save()
    bot.sendMessage(update.get_chat().get_id(), f'Сохранили тебя, {state.telegram_user.username}!')
    state.set_name('')


# @processor(state_manager, from_states='invalid_token')
# def hello_level_3(bot: TelegramBot, update: Update, state: TelegramState):
#     print('dfdfdfdfdfd')
#     bot.sendMessage(update.get_chat().get_id(), 'Прекрасно подделываешь токен, научи так же')
#     bot.sendMessage(update.get_chat().get_id(), f'Не пиши сюда больше, {state.telegram_user.username}! ')


# @processor(state_manager, from_states='fucking_talk')
# def hello_level_4(bot: TelegramBot, update: Update, state: TelegramState):
#     bot.sendMessage(update.get_chat().get_id(), f'Здарова, {state.telegram_user.username}! ')





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



