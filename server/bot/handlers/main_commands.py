import telegram
from telegram import Update, ReplyMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from KitchenWeb.parse_and_validations.parces import deep_link_parce
from KitchenWeb.parse_and_validations.validations import *
from bot.telegram_bot import TelegramBot

END = ConversationHandler.END
NEXTSTEP = range(1)


class MainCommandsHandler(TelegramBot):
    def __init__(self, dispatcher):
        super(MainCommandsHandler, self).__init__()
        self.dispatcher = dispatcher
        self.add_handlers()

    def add_handlers(self):
        self.dispatcher.add_handler(ConversationHandler(
                    entry_points=[CommandHandler('start', self.start)],
                    states={
                        NEXTSTEP: [MessageHandler(Filters.text & ~Filters.command, self.nextstep)]},
                    fallbacks=[CommandHandler('cancel', callback=[])]))
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('restart', self.restart))
        self.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.dispatcher.add_handler(CommandHandler('login', self.login))

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        text = update.message['text']
        reply_markup = telegram.ForceReply(force_reply=True, selective=False, input_field_placeholder='Имя')
        if '/start ' in text:
            org = is_organization(deep_link_parce(text))
            if org:
                if models.Employe.objects.filter(tg_user=update.message['chat']['username'], organization_id=org).exists():
                    self.send_message(recipient=chat_id, message='Вы уже прошли регистрацию.')
                else:
                    models.Employe.objects.create(
                        tg_user=update.message['chat']['username'],
                        tg_id=update.message['chat']['id'],
                        organization_id=org
                    )
                    self.send_message(recipient=chat_id, message=f'Добро пожаловать к боту! Мы успешно сохранили данные о Вас, {update.message["chat"]["username"]}, но перед тем, как пойти дальше, Вы должны указать Ваше имя следующим сообщением. Оно будет использоваться для подписи контейнеров с Вашей заказанной едой. В будущем Вы в любой момент сможете его изменить.', keyboard=reply_markup)
                    return NEXTSTEP
            else:
                self.send_message(recipient=chat_id, message='Ссылка невалидна!')
        else:
            self.send_message(recipient=chat_id, message='К сожалению мы не смогли найти ваш аккаунт. Пройдите регистрацию перейдя по ссылке, которую даст вам Никита.')

    def restart(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        self.send_message(recipient=chat_id, message=f'Привет, {update.message["chat"]["username"]}! Рады видеть Вас снова в KitchenBot!')

    def stop(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            tg_user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
            if tg_user.is_active:
                tg_user.is_active = False
                tg_user.save()
                self.send_message(recipient=chat_id, message='Рассылка отключена')
            else:
                self.send_message(recipient=chat_id, message='Рассылка уже отключена')
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message='К сожалению мы не смогли найти ваш аккаунт. Пройдите регистрацию перейдя по ссылке, которую даст вам Никита.')

    def login(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
            if models.UserToken.objects.filter(user=user).exists():
                self.send_message(recipient=chat_id, message='Вам уже был выделен токен.')
            else:
                models.UserToken.objects.create(user=user)
                token2 = models.UserToken.objects.get(user=user)
                self.send_message(recipient=chat_id, message=f'Прекрасно, держи свой линк на профиль : https://9af8f9261799.ngrok.io/accounts/{token2.key}')
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message='Вы не можете получить токен, пока не зарегестрируетесь по ссылке который должен был вам выдать Никита')

    def nextstep(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        tg_user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
        tg_user.username = update.message['text']
        tg_user.save()
        self.send_message(recipient=chat_id, message='Спасибо! Ваши данные сохранены!')
        return END

