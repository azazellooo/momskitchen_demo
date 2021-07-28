from django.core.exceptions import ObjectDoesNotExist
from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from accounts import models
from KitchenWeb.parse_and_validations import deep_link_parce, is_organization, is_user, deep_len_validator

DEEP_LINK = '/start '
STOP = '/stop'
START = '/start'
LOGIN = '/login'
ORGANIZATION_ID = None


@processor(state_manager,  from_states=state_types.All, update_types=update_types.Message, message_types=message_types.Text, success='iv', fail=state_types.Keep)
def hello_level_1(bot: TelegramBot, update: Update, state: TelegramState):
    state.reset_memory()
    if DEEP_LINK in update.message.text and deep_len_validator(update.message.text):
        ORGANIZATION_ID = deep_link_parce(update.message.text)
        org = is_organization(ORGANIZATION_ID)
        if org is not None:
            if models.Employe.objects.filter(tg_user=state.telegram_user, organization_id=org).exists():
                bot.sendMessage(update.get_chat().get_id(), f'Ты уже переходил мать его, {state.telegram_user.username}!')
                raise ProcessFailure
            else:
                models.Employe.objects.create(
                    tg_user=state.telegram_user,
                    organization_id=org
                )
                bot.sendMessage(update.get_chat().get_id(), f'Добро пожаловать к боту! Мы успешно сохранили данные о Вас, {state.telegram_user.username}, но перед тем, как пойти дальше, Вы должны указать Ваше имя следующим сообщением. Оно будет использоваться для подписи контейнеров с Вашей заказанной едой. В будущем Вы в любой момент сможете его изменить.')
                return
        else:
            bot.sendMessage(update.get_chat().get_id(), 'Прекрасно подделываешь токен, научи так же')
            bot.sendMessage(update.get_chat().get_id(), f'Не пиши сюда больше, {state.telegram_user.username}! ')
            raise ProcessFailure
    elif update.message.text == LOGIN:
        try:
            user = models.Employe.objects.get(tg_user=state.telegram_user)
            if models.UserToken.objects.filter(user=user).exists():
                bot.sendMessage(update.get_chat().get_id(), 'Вам уже был выделен токен')
                raise ProcessFailure
            else:
                models.UserToken.objects.create(user=user)
                token2 = models.UserToken.objects.get(user=user)
                bot.sendMessage(update.get_chat().get_id(), f'Прекрасно, держи свой линк на профиль : https://9af8f9261799.ngrok.io/accounts/{token2.key}')
                raise ProcessFailure
        except ObjectDoesNotExist:
            bot.sendMessage(update.get_chat().get_id(), 'Вы не можете получить токен, пока не зарегестрируетесь по токену который должен был вам выдать Никитыч ')
            raise ProcessFailure
    elif update.message.text == STOP:
        try:
            the_user = models.Employe.objects.get(tg_user=state.telegram_user)
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
            the_user = models.Employe.objects.get(tg_user=state.telegram_user)
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
        bot.sendMessage(update.get_chat().get_id(), f'Здарова, {state.telegram_user.username}! {update.get_chat().get_id()}')
        raise ProcessFailure


@processor(state_manager, from_states='iv')
def hello_level_2(bot, update, state):
    user = models.Employe.objects.get(tg_user=state.telegram_user)
    user.username = update.message.text
    user.save()
    bot.sendMessage(update.get_chat().get_id(), f'Сохранили тебя, {state.telegram_user.username}!')
    state.set_name('')
