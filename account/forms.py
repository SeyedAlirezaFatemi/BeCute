from django import forms

from barber.models import BarberShop
from customer.models import CustomUser


class SignupForm(forms.ModelForm):
    shop_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'type',
            'shop_name',
        )

    def clean(self):
        user_type, shop_name = self.cleaned_data.get('type'), self.cleaned_data.get('shop_name')
        if user_type == CustomUser.USER_TYPE_BARBER and not shop_name:
            self.add_error('shop_name', 'This field is required.')
        return self.cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        shop_name = data.pop('shop_name')
        user = CustomUser.objects.create_user(**data)
        BarberShop.objects.create(barber=user, name=shop_name)
        return user
