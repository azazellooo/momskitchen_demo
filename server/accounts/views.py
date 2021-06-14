from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView

from accounts.models import Users, UserToken


class UserProfileView(TemplateView):
    template_name = 'profile.html'
    def get(self, request, **kwargs):
        self.user = get_object_or_404(UserToken, key=kwargs['token'])
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.user
        return context