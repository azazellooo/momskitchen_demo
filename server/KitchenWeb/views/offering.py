from django.shortcuts import redirect, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView
import json

from KitchenWeb.forms import OfferingForm
from KitchenWeb.models import Offering


class OfferingCreateView(CreateView):
    model = Offering
    form_class = OfferingForm
    template_name = 'offering/create.html'
    context_object_name = 'offering'

    def get_success_url(self):
        return reverse('kitchen:category_list')


