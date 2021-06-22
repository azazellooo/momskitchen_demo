from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView
from KitchenWeb.forms import SearchForm
from KitchenWeb.models import Garnish
from django.db.models import Q
from django.utils.http import urlencode
import json


class GarnishListView(ListView):
    template_name = 'garnishes/list.html'
    model = Garnish
    context_object_name = 'garnishes'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(GarnishListView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data)
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
