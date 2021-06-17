from django import forms

from accounts.models import Users


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'is_active']