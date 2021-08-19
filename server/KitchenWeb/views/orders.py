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
    organizations = []

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
                        self.organizations.append(order.user.organization_id) if order.user.organization_id not in self.organizations else self.organizations
                        continue
            queryset = Order.objects.filter(id__in=to)
        else:
            queryset = Order.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['organizations'] = self.organizations
        context['order_data'] = {}
        context['total_sum'] = {}
        for org in self.organizations:
            context['order_data'][org] = {}
            context['total_sum'][org.name] = 0
        for order in context['object_list']:
            context['order_data'][order.user.organization_id][order.user] = {"order_offerings": {}, "carts": {}, "total_sum": 0}
            for order_offering in order.order_o.all():
                if order_offering.offering.date == self.date:
                    context['order_data'][order.user.organization_id][order.user]["order_offerings"][order_offering] = order_offering.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += order_offering.price
                    context['total_sum'][order.user.organization_id.name] += order_offering.price
            for cart in order.user.cart_user.all():
                if cart.offering.date == self.date and not cart.is_confirmed:
                    context['order_data'][order.user.organization_id][order.user]["carts"][cart] = cart.offering
                    context['order_data'][order.user.organization_id][order.user]["total_sum"] += cart.price
                    context['total_sum'][order.user.organization_id.name] += cart.price
        context['date'] = self.date
        return context


class OrderListViewForDate(PermissionMixin, ListView):
    model = Cart
    template_name = 'order/list.html'
    context_object_name = 'orders'
    organizations_list = []

    def get_queryset(self):
        to_be_excluded = []
        queryset = Cart.objects.all()
        for cart in queryset:
            if str(cart.offering.date) != self.kwargs['date']:
                to_be_excluded.append(cart.pk)
            else:
                if not cart.user.organization_id in self.organizations_list:
                    self.organizations_list.append(cart.user.organization_id)
        queryset.exclude(offering__in=to_be_excluded)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['date'] = self.kwargs['date']
        return context