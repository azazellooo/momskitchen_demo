from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView, UpdateView, ListView
from django.urls import reverse
from django.views.generic.list import MultipleObjectMixin
from KitchenWeb.mixin import PermissionMixin
from accounts.forms import EmployeeForm
from accounts.models import Employee, UserToken, BalanceChange, Review
from accounts.tasks import drop_time_token, validation_token


class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        slug = kwargs.get('slug')
        if kwargs:
            val_tok = validation_token(kwargs['token'])
            slug = kwargs.get('slug')
            if val_tok == True:
                status = UserToken.objects.get(key=kwargs['token'])
                if status.activated == False:
                    drop_time_token(kwargs['token'], request.session.session_key)
                    user_token = get_object_or_404(UserToken, key=kwargs['token'])
                    token = kwargs['token']
                    request.session['token'] = str(token)
                    user_token.activated = True
                    user_token.save()
                    if slug == 'to-offerings':
                        request.session['token'] = str(kwargs.get('token'))
                        return redirect('kitchen:menu')
                    return redirect('profile_distoken')
                else:
                    if slug == 'to-offerings':
                        request.session['token'] = str(kwargs.get('token'))
                        return redirect('kitchen:menu')
                    return redirect('disposability_error')
            else:
                return redirect('invalid_token')
        else:
            try:
                drop_time_token(request.session['token'], request.session.session_key)
                user_token = get_object_or_404(UserToken, key=request.session['token'])
                self.user = get_object_or_404(Employee, user_token=user_token)
            except KeyError:
                return HttpResponse('Unauthorized', status=401)

        return super().get(request, **kwargs)



    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.user
        context['active_orders'] = self.user.order_user.filter(is_delivered=False)
        context['orders'] = self.user.order_user.exclude(is_delivered=False)[0:5]
        return context


class UserUpdateView(UpdateView):
    template_name = 'accounts/update.html'
    form_class = EmployeeForm
    context_object_name = 'user'

    def get_object(self):
        drop_time_token(self.request.session['token'], self.request.session.session_key)
        self.user_token = get_object_or_404(UserToken, key=self.request.session['token'])
        self.user = get_object_or_404(Employee, user_token=self.user_token)
        return self.user

    def get_queryset(self):
        queryset = Employee.objects.filter(id=self.user.id)
        return queryset

    def get_success_url(self):
        return reverse('profile_distoken')


class EmployeeTransactionHistoryView(DetailView, MultipleObjectMixin):
    template_name = 'accounts/transaction_history.html'
    model = Employee
    paginate_by = 5
    paginate_orphans = 1
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        transactions = BalanceChange.objects.filter(employee=self.get_object()).order_by('-created_at')
        context = super(EmployeeTransactionHistoryView, self).get_context_data(object_list=transactions, **kwargs)
        return context

class ReviewListView(PermissionMixin, ListView):
    template_name = 'review/list.html'
    model = Review
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 1
    context_object_name = 'reviews'




