from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import Organization, BalanceChange, Employe
from django.views.generic import ListView, CreateView, UpdateView
from KitchenWeb.forms import SearchForm, OrganizationForm, BalanceChangeForm
from django.utils.http import urlencode


class OrganizationsListView(ListView):
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


class OrganizationCreateView(CreateView):
    model = Organization
    template_name = 'organizations/create.html'
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse('kitchen:organization-list')


class OrganizationDetailUpdateView(UpdateView):
    template_name = 'organizations/detail_update.html'
    model = Organization
    form_class = OrganizationForm
    context_object_name = 'organization'

    def get_success_url(self):
        return reverse('kitchen:organization-list')


class OrganizationBalancePageView(UpdateView):
    template_name = 'organizations/balance.html'
    model = Organization
    form_class = BalanceChangeForm

    def form_valid(self, form):
        employee = Employe.objects.get(pk=form.data.get('employee'))

        BalanceChange.objects.create(employe=employee,
                                     comment=form.data.get('comment'),
                                     type=form.data.get('type'),
                                     sum_balance=form.data.get('sum_balance'))
        if form.data.get('type') == 'accrual':
            employee.total_balance += int(form.data.get('sum_balance'))
            employee.save()
        else:
            employee.total_balance -= int(form.data.get('sum_balance'))
            employee.save()
        return redirect('kitchen:organization-balance', pk=self.kwargs.get('pk'))
