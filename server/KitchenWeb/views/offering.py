import json
from django.forms import model_to_dict
from django.shortcuts import reverse
from django.utils.http import urlencode
from django.views.generic import CreateView, ListView, UpdateView
from KitchenWeb.forms import OfferingForm, SearchForm
from KitchenWeb.mixin import PermissionMixin
from KitchenWeb.models import Offering


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
    paginate_by = 5
    paginate_orphans = 1

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
        needed_fields = ('id', 'name', 'description', 'category', 'base_price', 'offering_position', 'extra_price')
        dict_filter = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
        positions = []
        garnishes = []
        additionals = []
        context = super().get_context_data(**kwargs)
        for o in context.get('object_list'):
            if o.position.extra_price:
                o.position.extra_price = json.loads(o.position.extra_price)
            for garnish in list(o.garnish.all()):
                garnish_dict = dict_filter(model_to_dict(garnish), needed_fields)
                garnish_dict['offering'] = o.id
                garnishes.append(garnish_dict)
                if isinstance(garnish.extra_price, str):
                    garnish.extra_price = json.loads(garnish.extra_price)
                    garnish.save()
            for additional in o.additional.all():
                additional_dict = dict_filter(model_to_dict(additional), needed_fields)
                additional_dict['offering'] = o.id
                additionals.append(additional_dict)
                if isinstance(additional.extra_price, str):
                    additional.extra_price = json.loads(additional.extra_price)
                    additional.save()
                o.save()
        context['search_form'] = self.form
        context['to_js_offerings'] = {"offerings": list(context.get('offerings').values())}
        for o in context.get('offerings'):
            position = dict_filter(model_to_dict(o.position), needed_fields)
            position['offering'] = o.id
            positions.append(position)
        context['to_js_positions'] = {'positions': positions}
        context['to_js_garnishes'] = {'garnishes': garnishes}
        context['to_js_additionals'] = {'additionals': additionals}
        # context['to_json_positions'] = {'positions': [dict_filter(model_to_dict(o.position), needed) for o in list(context.get('offerings'))]}
        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})
        return context

    # def build_list(self, object_list,needed_fields, field: models.Model):
    #     dict_filter = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    #     field_list = []
    #     for o in object_list:
    #         print(field)
    #         expected_dict = dict_filter(model_to_dict(o.field), needed_fields)
    #         expected_dict['offering'] = o.id
    #         field_list.append(expected_dict)
    #     return field_list


class OfferingDetailUpdateView(UpdateView):
    template_name = 'offering/detail_update.html'
    model = Offering
    form_class = OfferingForm
    context_object_name = 'offering'

    def get_success_url(self):
        return reverse('kitchen:offering_list')



