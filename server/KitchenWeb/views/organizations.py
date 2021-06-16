from django.db.models import Q
from django.shortcuts import render
from accounts.models import Organization
from django.views.generic import ListView
from KitchenWeb.forms import SearchForm
from django.utils.http import urlencode


class OrganizationsListView(ListView):
    template_name = 'organizations/list.html'
    paginate_by = 5
    model = Organization
    paginate_orphans = 1
    context_object_name = 'organizations'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(OrganizationsListView, self).get(request, **kwargs)

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
