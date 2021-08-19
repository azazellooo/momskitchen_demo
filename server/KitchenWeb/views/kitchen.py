from django.db.models import Q
from django.urls import reverse
from KitchenWeb.models import Supplement
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from KitchenWeb.forms import SearchForm, SupplementForm
from django.utils.http import urlencode
from KitchenWeb.mixin import PermissionMixin


class SupplementListView(PermissionMixin, ListView):
    template_name = 'supplements/list.html'
    paginate_by = 5
    model = Supplement
    paginate_orphans = 1
    context_object_name = 'supplements'
    queryset = Supplement.objects.order_by('-created_at')

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(SupplementListView, self).get(request, **kwargs)

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


class SupplementCreateView(PermissionMixin, CreateView):
    template_name = 'supplements/create.html'
    model = Supplement
    form_class = SupplementForm

    def get_success_url(self):
        return reverse('kitchen:supplement-list')


class SupplementDetailUpdateView(PermissionMixin, UpdateView):
    model = Supplement
    template_name = 'supplements/detail_update.html'
    form_class = SupplementForm
    context_object_name = 'supplement'

    def get_success_url(self):
        return reverse('kitchen:detail_update_supplement', kwargs={'pk': self.object.pk})

