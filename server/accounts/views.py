from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView, UpdateView
from django.urls import reverse

from accounts.forms import EmployeForm
from accounts.models import Employe, UserToken
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
from accounts.tasks import drop_time_token, validation_token
from django.contrib.sessions.backends.db import SessionStore


class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        if kwargs:
            val_tok = validation_token(kwargs['token'])
            if val_tok == True:
                drop_time_token(kwargs['token'], request.session.session_key)
                user_token = get_object_or_404(UserToken, key=kwargs['token'])
                token = kwargs['token']
                request.session['token'] = str(token)
            else:
                raise KeyError
        else:
            drop_time_token(request.session['token'], request.session.session_key)
            user_token = get_object_or_404(UserToken, key=request.session['token'])
        self.user = get_object_or_404(Employe, user_token=user_token)
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.user
        return context


class UserUpdateView(UpdateView):
    template_name = 'accounts/update.html'
    form_class = EmployeForm
    context_object_name = 'user'

    def get_object(self):
        drop_time_token(self.request.session['token'], self.request.session.session_key)
        self.user_token = get_object_or_404(UserToken, key=self.request.session['token'])
        self.user = get_object_or_404(Employe, user_token=self.user_token)
        return self.user

    def get_queryset(self):
        queryset = Employe.objects.filter(id=self.user.id)
        return queryset

    def get_success_url(self):
        return reverse('profile_distoken')