from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, UpdateView

from KitchenWeb.forms import SearchForm, OrganizationForm, BalanceChangeForm
from KitchenWeb.mixin import PermissionMixin
from accounts.models import Organization, BalanceChange, Employee


class OrganizationsListView(PermissionMixin, ListView):
    template_name = 'organizations/list.html'
    paginate_by = 5
    model = Organization
    paginate_orphans = 1
    context_object_name = 'organizations'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(OrganizationsListView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data)
            )
        return queryset.filter(is_active=True)

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form


        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context


class OrganizationCreateView(PermissionMixin, CreateView):
    model = Organization
    template_name = 'organizations/create.html'
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse('kitchen:organization-list')


class OrganizationDetailUpdateView(PermissionMixin, UpdateView):
    template_name = 'organizations/detail_update.html'
    model = Organization
    form_class = OrganizationForm
    context_object_name = 'organization'

    def get_success_url(self):
        return reverse('kitchen:organization-list')


class OrganizationBalancePageView(PermissionMixin, UpdateView):
    template_name = 'organizations/balance.html'
    model = Organization
    form_class = BalanceChangeForm

    def form_valid(self, form):
        employee = Employee.objects.get(pk=form.data.get('employee'))
        comment = form.data.get('comment')
        sum_balance = int(form.data.get('sum_balance'))

        b = BalanceChange.objects.create(employee=employee,
                                     comment=comment,
                                     type=form.data.get('type'),
                                     sum_balance=form.data.get('sum_balance'))
        if form.data.get('type') == 'accrual':
            b.balance_after_transaction = employee.total_balance + sum_balance
            employee.total_balance += sum_balance
            employee.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 f'На счет сотрудника {employee.username} было начислено {sum_balance} сомов. Комментарий: {comment}')
        else:
            b.balance_after_transaction = employee.total_balance - sum_balance
            employee.total_balance -= int(form.data.get('sum_balance'))
            employee.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 f'Со счета сотрудника {employee.username} было снято {sum_balance} сомов. Комментарий: {comment}')
        b.save()
        return redirect('kitchen:organization-balance', pk=self.kwargs.get('pk'))
