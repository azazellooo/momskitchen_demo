from django import forms

from KitchenWeb.models import Supplement


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name', 'price']
