from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from KitchenWeb.forms import PositionForm
from KitchenWeb.models import Dish, Category
import json

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
        if form.data[str(len(TYPES))]:
            counter = len(TYPES)
            to_json = {}
            for key, value in form.data.items():
                if key.isnumeric():
                    to_json[value] = {"comment": (form.data.getlist(f'comment{counter}'))[0], "pricing": (form.data.getlist(f'pricing{counter}'))[0]}
                    counter -= 1
        json_var = json.dumps(to_json)
        position.extra_price = json_var
        position.save()
        return redirect('kitchen:organization-list')

    def get_success_url(self):
        return reverse('index')