from django import forms

from KitchenWeb.models import Supplement, Dish, Category, Garnish, Additional, Offering
from accounts.models import Organization, BalanceChange


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
        fields = ('name', 'description', 'category', 'image', 'base_price')


class GarnishForm(forms.ModelForm):

    class Meta:
        model = Garnish
        fields = ['name', 'order', 'base_price']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_name', 'order')


class AdditionalForm(forms.ModelForm):

    class Meta:
        model = Additional
        fields = ('name', 'sampling_order', 'base_price')


class DateInput(forms.DateInput):
    input_type = 'date'


class OfferingForm(forms.ModelForm):

    class Meta:
        model = Offering
        fields = ('position', 'garnish', 'additional', 'supplement', 'qty_portion', 'date')
        widgets = {
            'date': DateInput(),
        }


class BalanceChangeForm(forms.ModelForm):

    class Meta:
        model = BalanceChange
        fields = ('type', 'sum_balance', 'comment')
