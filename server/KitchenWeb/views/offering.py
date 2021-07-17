from django.utils.http import urlencode

from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, ListView, UpdateView
import json

from KitchenWeb.forms import OfferingForm, SearchForm
from KitchenWeb.models import Offering
from KitchenWeb.mixin import PermissionMixin

class OfferingCreateView(PermissionMixin, CreateView):
    model = Offering
    form_class = OfferingForm
    template_name = 'offering/create.html'
    context_object_name = 'offerings'

    def get_success_url(self):
        return reverse('kitchen:offering_list')


class OfferingListView(PermissionMixin, ListView):
    model = Offering
    template_name = 'offering/list.html'
    context_object_name = 'offerings'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(OfferingListView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                position__name__icontains=self.search_data
            )
        return queryset

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


class OfferingDetailUpdateView(UpdateView):
    template_name = 'offering/detail_update.html'
    model = Offering
    form_class = OfferingForm
    context_object_name = 'offering'

    def get_success_url(self):
        return reverse('kitchen:offering_list')
