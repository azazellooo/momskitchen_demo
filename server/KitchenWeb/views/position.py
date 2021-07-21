from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from KitchenWeb.forms import PositionForm, SearchForm
from KitchenWeb.models import Dish, Category
from django.db.models import Q
from django.utils.http import urlencode
import json
from KitchenWeb.mixin import PermissionMixin


class PositionListView(PermissionMixin, ListView):
    template_name = 'position/list.html'
    model = Dish
    paginate_by = 5
    paginate_orphans = 1
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


class PositionCreateView(PermissionMixin, CreateView):
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
                        to_json[value] = {"comment": (form.data.getlist(f'comment{counter}'))[0],
                                          "pricing": (form.data.getlist(f'pricing{counter}'))[0]}
                        counter -= 1
                json_var = json.dumps(to_json)
                position.extra_price = json_var
        except MultiValueDictKeyError:
            position.save()
        position.save()
        return redirect('kitchen:list_position')

    def get_success_url(self):
        return reverse('index')


class PositionDetailUpdateView(UpdateView):
    template_name = 'position/detail_update.html'
    model = Dish
    form_class = PositionForm
    context_object_name = 'position'

    def get_object(self, queryset=None):
        return get_object_or_404(Dish, pk=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        position = self.get_object()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        if position.extra_price:
            context['extra_price'] = json.loads(position.extra_price)
        if position.image:
            context['image'] = self.get_object().image
        return context

    def form_valid(self, form):
        print(form.data)
        print('----------------')
        print(form.cleaned_data)
        position = self.get_object()
        position.name = form.data['name']
        position.description = form.data['description']
        position.category = Category.objects.get(id=int(form.data['category']))
        position.base_price = int(form.data['base_price'])
        position.image = form.cleaned_data['image']
        try:
            to_json = {}
            for key, value in form.data.items():
                if "select" in key:
                    counter = int(key.replace('select', ""))
                    to_json[value] = {"comment": (form.data.get(f'comment{counter}')),
                                      "pricing": (form.data.get(f'pricing{counter}'))}
            json_var = json.dumps(to_json)
            position.extra_price = json_var
        except MultiValueDictKeyError:
            position.save()
        position.save()

        return redirect('kitchen:list_position')
