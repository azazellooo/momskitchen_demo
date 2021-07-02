from django import forms

from accounts.models import Employe


class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['username', 'is_active']