import telegram
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from KitchenWeb.parse_and_validations.parces import deep_link_parce, review_text_parse
from KitchenWeb.parse_and_validations.validations import *
from accounts.models import Review
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
        self.dispatcher.add_handler(CommandHandler('review', self.review))

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        text = update.message.text
        reply_markup = telegram.ForceReply(force_reply=True, selective=False, input_field_placeholder='Имя')
        if '/start ' in text:
            org = is_organization(deep_link_parce(text))
            if org:
                if models.Employee.objects.filter(
                        tg_id=chat_id, organization_id=org
                ).exists():
                    self.send_message(recipient=chat_id, message=USER_ALREADY_SIGNED_UP)
                else:
                    models.Employee.objects.create(
                        tg_username=update.message.chat.username,
                        tg_id=chat_id,
                        organization_id=org
                    )
                    self.send_message(recipient=chat_id, message=WELCOME[0]+update.message.chat.username+WELCOME[1], keyboard=reply_markup)
                    return NEXTSTEP
            else:
                self.send_message(recipient=chat_id, message=INVALID_LINK)
        else:
            if models.Employee.objects.filter(
                    tg_id=chat_id
            ).exists():
                self.send_message(recipient=chat_id, message=BOT_ALREADY_STARTED)
            else:
                self.send_message(recipient=chat_id, message=USER_NOT_FOUND)


    def restart(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            tg_user = models.Employee.objects.get(tg_id=chat_id)
            if not tg_user.is_active:
                tg_user.is_active = True
                tg_user.save()
                self.send_message(
                    recipient=chat_id, message=WELCOME_BACK[0] + update.message.chat.username + WELCOME_BACK[1]
                )
            else:
                self.send_message(recipient=chat_id, message=ALREADY_ACTIVE)
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message=USER_NOT_FOUND)

    def stop(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            tg_user = models.Employee.objects.get(tg_id=chat_id)
            if tg_user.is_active:
                tg_user.is_active = False
                tg_user.save()
                self.send_message(recipient=chat_id, message=MAILING_OFF)
            else:
                self.send_message(recipient=chat_id, message=MAILING_ALREADY_OFF)
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message=USER_NOT_FOUND)

    def login(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        try:
            user = models.Employee.objects.get(tg_id=chat_id)
            if models.UserToken.objects.filter(user=user).exists():
                self.send_message(recipient=chat_id, message=TOKEN_ALREADY_GIVEN)
            else:
                models.UserToken.objects.create(user=user)
                token2 = models.UserToken.objects.get(user=user)
                self.send_message(recipient=chat_id, message=GIVE_TOKEN+str(token2.key)+'/')
        except ObjectDoesNotExist:
            self.send_message(recipient=chat_id, message=CANNOT_GIVE_TOKEN)

    def nextstep(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        tg_user = models.Employee.objects.get(tg_id=chat_id)
        tg_user.username = update.message.text
        tg_user.save()
        self.send_message(recipient=chat_id, message=DATA_SAVED)
        return END


    def review(self, update: Update, context:CallbackContext):
        chat_id = update.message.chat.id
        if models.Employee.objects.filter(tg_id=chat_id).exists():
            text = review_text_parse(update.message.text)
            employee = models.Employee.objects.get(tg_id=chat_id)
            review = Review.objects.create(user_name=employee, text_review=text)
            self.send_message(recipient=chat_id, message=REVIEW_SUCCESS)
            for admin in models.Employee.objects.filter(is_admin=True):
                self.send_message(recipient=chat_id, message=text)
                self.send_message(recipient=admin.tg_id, message=REVIEW_ADMIN_SUCCESS + text)
        else:
            self.send_message(recipient=chat_id, message=USER_NOT_FOUND)