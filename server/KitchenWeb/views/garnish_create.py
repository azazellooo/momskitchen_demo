from django.shortcuts import redirect, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView
import json

from KitchenWeb.forms import GarnishForm
from KitchenWeb.models import Garnish



TYPES = [0.3, 0.5, 0.7, 1.3, 1.5, 1.7, 2]

class GarnishCreateView(CreateView):
    model = Garnish
    form_class = GarnishForm
    template_name = 'garnishes/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = TYPES
        return context

    def form_valid(self, form):
        garnish = Garnish()
        garnish.name = form.data['name']
        garnish.order = form.data['order']
        garnish.base_price = int(form.data['base_price'])

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
            garnish.extra_price = json_var
        except MultiValueDictKeyError:
            garnish.save()
        garnish.save()
        return redirect('kitchen:organization-list')

    def get_success_url(self):
        return reverse('index')




