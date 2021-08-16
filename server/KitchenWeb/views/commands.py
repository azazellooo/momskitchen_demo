from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView

from telegram import ParseMode
from telegram.constants import PARSEMODE_MARKDOWN, PARSEMODE_HTML
from telegram.error import BadRequest

from KitchenWeb.forms import OrderCreateForm, OrderCloseForm, OrderReminderForm, NotificationForm, DeliveryArrivalForm
from accounts.models import Organization, UserToken, Employee
from bot.telegram_bot import TelegramBot

BASE_URL = 'https://f6ea2a483fd1.ngrok.io'
bot = TelegramBot()
today = date.today()


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

    def announce_new_offering(self, organizations, optional_text):
        for org_id in organizations:
            org = Organization.objects.get(id=org_id)
            for employee in org.employe_org.filter(is_active=True):
                link = self.generate_link_to_offerings(employee)
                bot.send_message(recipient=employee.tg_id,
                                 message=f"Заказ на эту дату уже создан, скорее <a href='{link}'>заходи</a>! {optional_text[0]}", parse_mode=ParseMode.HTML)
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        messages.add_message(self.request, messages.SUCCESS, f'отправлено уведомление о новом предложении организациям: {org_names}')

    def notify(self, organizations, optional_text):
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        for org in organizations:
            for employee in Organization.objects.get(id=org).employe_org.filter(is_active=True):
                # try:
                bot.send_message(recipient=employee.tg_id, message=optional_text, parse_mode=PARSEMODE_MARKDOWN)
                messages.add_message(self.request, messages.SUCCESS,
                                     f'отправлено уведомление {optional_text[0]} организациям: {org_names}')
                # except BadRequest:
                #     messages.add_message(self.request, messages.ERROR, 'сообщение не отправлено')

    def remind(self, organizations, optional_text):
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        for org_id in organizations:
            org = Organization.objects.get(id=org_id)
            print(org)

            for employee in org.employe_org.filter(is_active=True, cart_user__is_confirmed=False):
                print(org)
                link = self.generate_link_to_offerings(employee)
                bot.send_message(recipient=employee.tg_id,
                                 message=f"Зака на {employee.cart_user.first().offering.date} закроется, <a href='{link}'>поторопись</a> ! {optional_text[0]}",
                                 parse_mode=ParseMode.HTML)
                messages.add_message(self.request, messages.SUCCESS,
                                     f'отправлено напоминание о закрытии заказа на дату {employee.cart_user.first().offering.date} организациям: {org_names}',)


    def delivery_arrival(self, organizations, optional_text):
        org_names = [Organization.objects.get(id=o).name for o in organizations]
        for org_id in organizations:
            org = Organization.objects.get(id=org_id)

            employees = org.employe_org.filter(is_active=True, order_user__created_at__date=today, order_user__is_delivered=False)
            for employee in employees:
                orders = employee.order_user.filter(created_at__date=today, is_delivered=False)
                total = 0
                for order in orders:
                    for item in order.order_o.all():
                        total += item.price
                    order.is_delivered = True
                    order.save()
                if not (org.payment == 'cumulative' and employee.total_balance > 0) or org.payment == 'actual':
                    message = f'Заказ уже приехал! Не забудьте оплатить {total} сом. {optional_text[0]}'
                else:
                    message = f'Заказ уже приехал! {optional_text[0]}'
                bot.send_message(recipient=employee.tg_id, message=message)
                messages.add_message(self.request, messages.SUCCESS,
                                     f'отправлено уведомление о прибытии доставки организациям: {org_names}')

    def post(self, request, *args, **kwargs):
        post_data = dict(request.POST)
        post_data_list = list(post_data)
        if 'notification_form-organization' in post_data_list:
            self.notify(post_data.get('notification_form-organization'), post_data.get('notification_form-text')[0])
        if 'create_form-organization' in post_data_list:
            self.announce_new_offering(post_data.get('create_form-organization'), post_data.get('create_form-text'))
        if 'reminder_form-organization' in post_data_list:
            self.remind(post_data.get('reminder_form-organization'), post_data.get('reminder_form-text'))
        if 'delivery_arrival-organization' in post_data_list:
            self.delivery_arrival(post_data.get('delivery_arrival-organization'), post_data.get('delivery_arrival-text'))
        return redirect(reverse("kitchen:commands"))
