from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView

from telegram import ParseMode

from KitchenWeb.forms import OrderCreateForm, OrderCloseForm, OrderReminderForm, NotificationForm, DeliveryArrivalForm
from accounts.models import Organization, UserToken, Employee
from bot.telegram_bot import TelegramBot

BASE_URL = 'https://d23a719c76f9.ngrok.io'
bot = TelegramBot()


class CommandSendView(TemplateView):
    template_name = 'commands/commands.html'

    def get(self, request, *args, **kwargs):
        create_form = OrderCreateForm(self.request.GET or None, prefix="create_form")
        close_form = OrderCloseForm(self.request.GET or None, prefix='close_form')
        reminder_form = OrderReminderForm(self.request.GET or None, prefix='reminder_form')
        notification_form = NotificationForm(self.request.GET or None, prefix='notification_form')
        delivery_arrival = DeliveryArrivalForm(self.request.GET or None, prefix='delivery_arrival')
        context = super(CommandSendView, self).get_context_data(**kwargs)
        context['create_form'] = create_form
        context['close_form'] = close_form
        context['reminder_form'] = reminder_form
        context['notification_form'] = notification_form
        context['delivery_arrival'] = delivery_arrival
        return render(request, self.template_name, context=context)

    def generate_link_to_offerings(self, employee):
        try:
            token = employee.user_token
        except Employee.user_token.RelatedObjectDoesNotExist:
            token = UserToken.objects.create(user=employee)
        if token.activated:
            token.delete()
            token = UserToken.objects.create(user=employee)
        return f'{BASE_URL}/accounts/{token.key}/to-offerings'

    def announce_new_offering(self, organizations, message):
        for org_id in organizations:
            org = Organization.objects.get(id=org_id)
            for employee in org.employe_org.filter(is_active=True):
                link = self.generate_link_to_offerings(employee)
                bot.send_message(recipient=employee.tg_id,
                                 message=f"Заказ на эту дату уже создан, скорее <a href='{link}'>заходи</a>! {message[0]}", parse_mode=ParseMode.HTML)
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        messages.add_message(self.request, messages.SUCCESS, f'отправлено уведомление о новом предложении организациям: {org_names}')

    def notify(self, organizations, message):
        for org in organizations:
            for employee in Organization.objects.get(id=org).employe_org.filter(is_active=True, is_admin=False):
                bot.send_message(recipient=employee.tg_id, message=message)
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        messages.add_message(self.request, messages.SUCCESS, f'отправлено уведомление {message} организациям: {org_names}')

    def post(self, request, *args, **kwargs):
        post_data = dict(request.POST)
        if 'notification_form-organization' in list(post_data):
            self.notify(post_data.get('notification_form-organization'), post_data.get('notification_form-text')[0])
        if 'create_form-organization' in list(post_data):
            self.announce_new_offering(post_data.get('create_form-organization'), post_data.get('create_form-text'))
        return redirect(reverse("kitchen:commands"))
