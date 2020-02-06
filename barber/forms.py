from django import forms


class BarberShopSearchForm(forms.Form):
    search_text = forms.CharField(
        required=True,
        label='Search name',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )


class AddServiceToBarbershop(forms.Form):
    service_name = forms.CharField(max_length=50, required=True)
    price = forms.DecimalField(required=True)
    duration = forms.DurationField(required=True)
    discounted_price = forms.DecimalField(required=False)
