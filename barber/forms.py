from django import forms


class BarberShopSearchForm(forms.Form):
    search_text = forms.CharField(
        required=True,
        label='Search name',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )
