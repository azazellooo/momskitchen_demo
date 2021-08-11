from django.shortcuts import redirect
from KitchenWeb.forms import SearchForm
from KitchenWeb.models import Offering
from KitchenWeb.views.offering import OfferingListView
from datetime import datetime



class OfferingListViewForDate(OfferingListView):
    model = Offering
    template_name = 'offering/list.html'
    context_object_name = 'offerings'
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, **kwargs):
        now = datetime.now().date()
        if datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date() < now:
            return redirect('kitchen:offering_list')
        else:
            self.form = SearchForm(request.GET)
            self.search_data = self.get_search_data()
            return super(OfferingListViewForDate, self).get(request, **kwargs)

    def get_queryset(self):
        needed_date = self.kwargs['date']
        queryset = Offering.objects.filter(date__exact=needed_date)
        if self.search_data:
            queryset = queryset.filter(
                position__name__icontains=self.search_data
            )
        return queryset