from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, UpdateView
from django.urls import reverse

from accounts.forms import UsersForm
from accounts.models import Users, UserToken




class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        user_token = get_object_or_404(UserToken, key=kwargs['token'])
        self.user = get_object_or_404(Users, user_token=user_token)
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.user
        return context


class UserUpdateView(UpdateView):
    template_name = 'accounts/update.html'
    form_class = UsersForm
    context_object_name = 'user'

    def get_object(self):
        self.user_token = get_object_or_404(UserToken, key=self.kwargs['token'])
        self.user = get_object_or_404(Users, user_token=self.user_token)
        return self.user

    def get_queryset(self):
        queryset = Users.objects.filter(id=self.user.id)
        return queryset

    def get_success_url(self):
        return reverse('organizations:list')

