import json
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.http import urlencode
from django.views.generic import ListView, UpdateView
from KitchenWeb.forms import SearchForm, GarnishForm
from KitchenWeb.mixin import PermissionMixin
from KitchenWeb.models import Garnish

TYPES = [0.3, 0.5, 0.7, 1.3, 1.5, 1.7, 2]


class GarnishListView(PermissionMixin, ListView):
    template_name = 'garnishes/list.html'
    model = Garnish
    paginate_by = 5
    paginate_orphans = 1
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


class GarnishDetailUpdateView(PermissionMixin, UpdateView):
    template_name = 'garnishes/detail_update.html'
    model = Garnish
    form_class = GarnishForm
    context_object_name = 'garnish'

    def get_object(self, queryset=None):
        return get_object_or_404(Garnish, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        garnish = self.get_object()
        garnish.name = form.data['name']
        garnish.order = form.data['order']
        garnish.base_price = form.data['base_price']
        try:
            to_json = {}
            for key, value in form.data.items():
                if "select" in key:
                    counter = int(key.replace('select', ""))
                    to_json[value] = {"comment": (form.data.get(f'comment{counter}')),
                                      "pricing": (form.data.get(f'pricing{counter}'))}
            json_var = json.dumps(to_json, ensure_ascii=False)

            garnish.extra_price = json_var
        except MultiValueDictKeyError:
            garnish.save()
        garnish.save()
        return redirect('kitchen:list_garnish')

    def get_context_data(self, *, object_list=None, **kwargs):
        garnish = self.get_object()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        if garnish.extra_price:
            if isinstance(garnish.extra_price, str):
                context['extra_price'] = json.loads(garnish.extra_price)
        return context

