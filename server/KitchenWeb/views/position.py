from django.shortcuts import redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, ListView, UpdateView
from KitchenWeb.forms import PositionForm, SearchForm
from KitchenWeb.models import Dish, Category
from django.db.models import Q
from django.utils.http import urlencode
import json


class PositionListView(ListView):
    template_name = 'position/list.html'
    model = Dish
    context_object_name = 'dishes'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(PositionListView, self).get(request, **kwargs)

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


TYPES = [0.5, 0.7]


class PositionCreateView(CreateView):
    template_name = 'position/create.html'
    form_class = PositionForm
    model = Dish

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        return context

    def form_valid(self, form):
        position = Dish()
        position.name = form.data['name']
        position.description = form.data['description']
        position.category = Category.objects.get(id=int(form.data['category']))
        position.base_price = int(form.data['base_price'])
        position.image = form.cleaned_data['image']
        try:
            if form.data[str(len(TYPES))]:
                counter = len(TYPES)
                to_json = {}
                for key, value in form.data.items():
                    if key.isnumeric():
                        to_json[value] = {"comment": (form.data.getlist(f'comment{counter}'))[0], "pricing": (form.data.getlist(f'pricing{counter}'))[0]}
                        counter -= 1
                json_var = json.dumps(to_json)
                position.extra_price = json_var
        except MultiValueDictKeyError:
            position.save()
        position.save()
        return redirect('kitchen:organization-list')

    def get_success_url(self):
        return reverse('index')
