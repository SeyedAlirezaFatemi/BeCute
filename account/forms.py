from django import forms

from barber.models import BarberShop
from customer.models import CustomUser


class SignupForm(forms.ModelForm):
    shop_name = forms.CharField(max_length=100, required=False)
    introduction = forms.CharField(max_length=1000, required=False)
    address = forms.CharField(max_length=1000, required=False)
    city = forms.CharField(max_length=100, required=False)
    foundation_year = forms.CharField(required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "type",
            "shop_name",
            "introduction",
            "address",
            "city",
            "foundation_year",
            "phone"
        )

    def clean(self):
        user_type, shop_name = (
            self.cleaned_data.get("type"),
            self.cleaned_data.get("shop_name"),
        )
        if user_type == CustomUser.USER_TYPE_BARBER and not shop_name:
            self.add_error("shop_name", "This field is required.")
        return self.cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        shop_name = data.pop("shop_name")
        introduction = data.pop("introduction")
        address = data.pop("address")
        city = data.pop("city")
        foundation_year = data.pop("foundation_year")
        phone = data.pop("phone")
        user_created = CustomUser.objects.create_user(data.pop("username"), data.pop("email"), data.pop("password"), **data)
        if data.get("type") == CustomUser.USER_TYPE_BARBER:
            BarberShop.objects.create(barber=user_created, name=shop_name, introduction=introduction, city=city, address=address, foundation_year=foundation_year, phone=phone)
        return user_created
