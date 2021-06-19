from django import forms

from KitchenWeb.models import Supplement, Dish, Category
from accounts.models import Organization


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name', 'price']


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'leave_review', 'address', 'is_active', 'payment', 'bonus_activation', ]


class PositionForm(forms.ModelForm):

    class Meta:
        model = Dish
        category = forms.ModelChoiceField(queryset=Category.objects.all())
        fields = ('name','description', 'category', 'image', 'base_price')