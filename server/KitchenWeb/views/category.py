from django.urls import reverse
from django.views.generic import ListView, CreateView
from KitchenWeb.models import Category
from KitchenWeb.forms import SearchForm, CategoryForm
from django.utils.http import urlencode
from django.db.models import Q


class CategoryListView(ListView):
    template_name = 'category/list.html'
    paginate_by = 5
    model = Category
    paginate_orphans = 1
    context_object_name = 'categories'

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(CategoryListView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(category_name__icontains=self.search_data)
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


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category/create.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('kitchen:category_list')