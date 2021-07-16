from django import forms
from django.forms import TextInput, EmailInput

from KitchenWeb.models import Supplement, Dish, Category, Garnish, Additional, Offering
from accounts.models import Organization, BalanceChange


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')


class SupplementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SupplementForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Supplement
        fields = ['name', 'price']


class OrganizationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Organization
        fields = ['name', 'leave_review', 'address', 'is_active', 'payment', 'bonus_activation', ]


class PositionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Dish
        category = forms.ModelChoiceField(queryset=Category.objects.all())
        fields = ('name', 'description', 'category', 'image', 'base_price', 'extra_price')


class GarnishForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GarnishForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})


    class Meta:
        model = Garnish
        fields = ['name', 'order', 'base_price', 'extra_price']



class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Category
        fields = ('category_name', 'order')


class AdditionalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdditionalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Additional
        fields = ('name', 'sampling_order', 'base_price', 'extra_price')


class OfferingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OfferingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Offering
        fields = ('position', 'garnish', 'additional', 'supplement', 'date', 'qty_portion')


class BalanceChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BalanceChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = BalanceChange
        fields = ('type', 'sum_balance', 'comment')





