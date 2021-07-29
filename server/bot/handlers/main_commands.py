import telegram
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from KitchenWeb.parse_and_validations.parces import deep_link_parce
from KitchenWeb.parse_and_validations.validations import *
from bot.telegram_bot import TelegramBot
from messages.bot_messages import *

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
                if models.Employe.objects.filter(
                        tg_user=update.message['chat']['username'], organization_id=org
                ).exists():
                    self.send_message(recipient=chat_id, message=user_already_signed_up)
                else:
                    models.Employe.objects.create(
                        tg_user=update.message['chat']['username'],
                        tg_id=update.message['chat']['id'],
                        organization_id=org
                    )
                    self.send_message(recipient=chat_id, message=welcome[0]+{update.message["chat"]["username"]}+welcome[1], keyboard=reply_markup)
                    return NEXTSTEP
            else:
                self.send_message(recipient=chat_id, message=invalid_link)
        else:
            self.send_message(recipient=chat_id, message=user_not_found)

    def restart(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        self.send_message(
            recipient=chat_id, message=welcome_back[0]+{update.message["chat"]["username"]}+welcome_back[1]
        )

    def stop(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            tg_user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
            if tg_user.is_active:
                tg_user.is_active = False
                tg_user.save()
                self.send_message(recipient=chat_id, message=mailing_off)
            else:
                self.send_message(recipient=chat_id, message=mailing_already_off)
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message=user_not_found)

    def login(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
            if models.UserToken.objects.filter(user=user).exists():
                self.send_message(recipient=chat_id, message=token_already_given)
            else:
                models.UserToken.objects.create(user=user)
                token2 = models.UserToken.objects.get(user=user)
                self.send_message(recipient=chat_id, message=give_token+{token2.key})
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message=cannot_give_token)

    def nextstep(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        tg_user = models.Employe.objects.get(tg_user=update.message["chat"]["username"])
        tg_user.username = update.message['text']
        tg_user.save()
        self.send_message(recipient=chat_id, message=data_saved)
        return END

