import json
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, UpdateView

from KitchenWeb.forms import SearchForm, AdditionalForm
from KitchenWeb.mixin import PermissionMixin
from KitchenWeb.models import Additional
from KitchenWeb.views.garnish import TYPES

TYPES = [0.3, 0.5, 0.7, 1.3, 1.5, 1.7, 2]


class AdditionalListView(PermissionMixin, ListView):
    template_name = 'additional/list.html'
    paginate_by = 5
    model = Additional
    paginate_orphans = 1
    context_object_name = 'additionals'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(AdditionalListView, self).get(request, **kwargs)

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


class AdditionalCreateView(PermissionMixin, CreateView):
    template_name = 'additional/create.html'
    model = Additional
    form_class = AdditionalForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        return context

    def form_valid(self, form):
        additional = Additional()
        additional.name = form.data['name']
        additional.sampling_order = form.data['sampling_order']
        additional.base_price = int(form.data['base_price'])
        try:
            if form.data[str(len(TYPES))]:
                counter = len(TYPES)
                to_json = {}
                for key, value in form.data.items():
                    if key.isnumeric():
                        to_json[value] = {
                            "comment": (form.data.getlist(f'comment{counter}'))[0],
                            "pricing": (form.data.getlist(f'pricing{counter}'))[0]
                        }
                        counter -= 1
                json_var = json.dumps(to_json)
            additional.extra_price = json_var
        except MultiValueDictKeyError:
            additional.save()
        additional.save()
        return redirect('kitchen:additional_list')


class AdditionalDetailUpdateView(PermissionMixin, UpdateView):
    template_name = 'additional/detail_update.html'
    model = Additional
    form_class = AdditionalForm
    context_object_name = 'additional'

    def get_object(self, queryset=None):
        return get_object_or_404(Additional, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        additional = self.get_object()
        additional.name = form.data['name']
        additional.sampling_order = form.data['sampling_order']
        additional.base_price = form.data['base_price']
        try:
            to_json = {}
            for key, value in form.data.items():
                if "select" in key:
                    counter = int(key.replace('select', ""))
                    to_json[value] = {"comment": (form.data.get(f'comment{counter}')),
                                      "pricing": (form.data.get(f'pricing{counter}'))}
            json_var = json.dumps(to_json)
            additional.extra_price = json_var
        except MultiValueDictKeyError:
            additional.save()
        additional.save()
        return redirect('kitchen:additional_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        additional = self.get_object()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        if additional.extra_price:
            if isinstance(additional.extra_price, str):
                context['extra_price'] = json.loads(additional.extra_price)
        return context