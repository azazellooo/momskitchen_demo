from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, EmailInput
from markdownx.fields import MarkdownxFormField
from KitchenWeb.models import Supplement, Dish, Category, Garnish, Additional, Offering, Command
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
        fields = ('name', 'description', 'category', 'image', 'base_price')


class GarnishForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GarnishForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})


    class Meta:
        model = Garnish
        fields = ['name', 'order', 'base_price']



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
        fields = ('name', 'sampling_order', 'base_price')


class AdditionalUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdditionalUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Additional
        fields = ('name', 'sampling_order', 'base_price')


class DateInput(forms.DateInput):
    input_type = 'date'


class OfferingForm(forms.ModelForm):
    garnish = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Гарниры',
        queryset=Garnish.objects.all()
    )
    additional = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Дополнения',
        queryset=Additional.objects.all()
    )
    supplement = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Надбавки',
        queryset=Supplement.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(OfferingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px; list-style: none'})

    class Meta:
        model = Offering
        fields = ('position', 'garnish', 'additional', 'supplement', 'qty_portion', 'date')
        widgets = {
            'date': DateInput()

        }



class OfferingCreateView(OfferingForm):

    def clean_position(self):
        position = self.cleaned_data.get('position')
        date = self.data.get('date')
        if Offering.objects.filter(position=position, date=date).exists():
            raise ValidationError(f"предложение на дату {date} с такой позицией уже есть( ")
        return position



class BalanceChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BalanceChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = BalanceChange
        fields = ('type', 'sum_balance', 'comment')


class OrderCreateForm(forms.ModelForm):
    organization = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Организации',
        queryset=Organization.objects.all()
    )
    text = forms.CharField(label='Текст')

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Command
        fields = ('organization', 'text')


class OrderReminderForm(forms.ModelForm):
    organization = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Организации',
        queryset=Organization.objects.all()
    )
    text = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(OrderReminderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Command
        fields = ('organization', 'text')


class OrderCloseForm(forms.ModelForm):
    organization = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Организации',
        queryset=Organization.objects.all()
    )
    text = forms.CharField(label='Текст')

    def __init__(self, *args, **kwargs):
        super(OrderCloseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Command
        fields = ('organization',)


class DeliveryArrivalForm(forms.ModelForm):
    organization = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Организации',
        queryset=Organization.objects.all()
    )
    text = forms.CharField(label='Текст')

    def __init__(self, *args, **kwargs):
        super(DeliveryArrivalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width: 300px;'})

    class Meta:
        model = Command
        fields = ('organization', 'text')


class NotificationForm(forms.ModelForm):
    organization = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Организации',
        queryset=Organization.objects.all()
    )
    text = MarkdownxFormField(label='Текст')

    class Meta:
        model = Command
        fields = ('organization', 'text')
