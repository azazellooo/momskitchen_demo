from django.shortcuts import render
from django.views.generic import TemplateView, FormView


from KitchenWeb.forms import OrderCreateForm, OrderCloseForm, OrderReminderForm, NotificationForm, DeliveryArrivalForm

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

