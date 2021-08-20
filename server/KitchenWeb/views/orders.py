from datetime import datetime
from django.views.generic import ListView
from KitchenWeb.mixin import PermissionMixin
from KitchenWeb.models import Cart
from KitchenWeb.models import Order


class OrderListView(PermissionMixin, ListView):
    model = Order
    template_name = 'order/list.html'
    context_object_name = 'orders'
    date = None
    organizations = {}

    def get_queryset(self):
        now = datetime.now().date()
        queryset = Order.objects.all()
        to = []
        dates = []
        for order in queryset:
            for order_offering in order.order_o.all():
                if order_offering.offering.date >= now:
                    dates.append(order_offering.offering.date)
        if dates:
            self.date = min(dates, key=lambda sub: abs(sub - now))
            for order in queryset:
                for order_offering in order.order_o.all():
                    if order_offering.offering.date == self.date:
                        to.append(order.pk)
                        self.organizations[order.user.organization_id] = 0
                        continue
            queryset = Order.objects.filter(id__in=to)
        else:
            queryset = Order.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['organizations'] = self.organizations
        context['order_data'] = {}
        context['dates'] = []
        dates = []
        order_offerings = []
        now = datetime.now().date()
        counter = 0
        for org in context['organizations']:
            context['order_data'][org] = {}
        for order in context['object_list']:
            context['order_data'][order.user.organization_id][order.user] = {"order_offerings": {}, "carts": {}, "total_sum": 0}
            for order_offering in order.order_o.all():
                dates.append(order_offering.offering.date)
                if order_offering.offering.date == self.date:
                    context['order_data'][order.user.organization_id][order.user]["order_offerings"][order_offering] = order_offering.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += order_offering.price
                    order_offerings.append(order_offering)
            for cart in order.user.cart_user.all():
                if cart.offering.date == self.date and not cart.is_confirmed:
                    context['order_data'][order.user.organization_id][order.user]["carts"][cart] = cart.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += cart.price
                    order_offerings.append(cart)
            self.organizations[order.user.organization_id] = order.total_sum(order_offerings)
        context['date'] = self.date
        if dates:
            result_date = min(dates, key=lambda sub: abs(sub - now))
            for order in Order.objects.all():
                for order_offering in order.order_o.all():
                    if order_offering.offering.date > result_date and counter < 5:
                        context['dates'].append(str(order_offering.offering.date)) if str(order_offering.offering.date) not in context['dates'] else context['dates']
                        counter += 1
            context['date'] = result_date
        return context


class OrderListViewForDate(OrderListView):
    organizations = {}

    def get_queryset(self):
        to_be_filtered = []
        queryset = Order.objects.all()
        self.date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        for order in queryset:
            for order_offering in order.order_o.all():
                if order_offering.offering.date == self.date:
                    to_be_filtered.append(order.pk)
                    if not order.user.organization_id in self.organizations:
                        self.organizations[order.user.organization_id] = 0
        queryset = queryset.filter(id__in=to_be_filtered)
        return queryset

    def get_context_data(self, **kwargs):
        context = {'organizations': self.organizations, 'order_data': {}}
        order_offerings = []
        for org in context['organizations']:
            context['order_data'][org] = {}
        orders = self.get_queryset()
        for order in orders:
            context['order_data'][order.user.organization_id][order.user] = {"order_offerings": {}, "carts": {}, "total_sum": 0}
            for order_offering in order.order_o.all():
                if order_offering.offering.date == self.date:
                    context['order_data'][order.user.organization_id][order.user]["order_offerings"][order_offering] = order_offering.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += order_offering.price
                    order_offerings.append(order_offering)
            for cart in order.user.cart_user.all():
                if cart.offering.date == self.date and not cart.is_confirmed:
                    context['order_data'][order.user.organization_id][order.user]["carts"][cart] = cart.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += cart.price
                    order_offerings.append(cart)
            self.organizations[order.user.organization_id] = order.total_sum(order_offerings)
        context['date'] = self.date
        return context

