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
    about_me = forms.CharField(max_length=200, required=False)
    # gender = forms.ChoiceField(required=False)
    age = forms.IntegerField(required=False)
    residence_city = forms.CharField(required=False)
    phone_customer = forms.IntegerField(required=False)
    # hair_type = forms.ChoiceField(required=False)

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
            "phone",
            "about_me",
            "gender",
            "age",
            "residence_city",
            "phone_customer",
            "hair_type",
        )

    def clean(self):
        user_type, shop_name = (
            self.cleaned_data.get("type"),
            self.cleaned_data.get("shop_name"),
        )
        if user_type == CustomUser.USER_TYPE_BARBER and not shop_name:
            self.add_error("shop_name", "Shop's name is required.")
        phone_customer, phone = (self.cleaned_data.get("phone_customer"),
                                 self.cleaned_data.get("phone"))
        if user_type == CustomUser.USER_TYPE_CLIENT:
            if not str(phone_customer).isdecimal():
                self.add_error("phone_customer", "Enter a correct phone number")
        elif user_type == CustomUser.USER_TYPE_BARBER:
            if not str(phone).isdecimal():
                self.add_error("phone", "Enter a correct phone number")
        return self.cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        shop_name = data.pop("shop_name")
        introduction = data.pop("introduction")
        address = data.pop("address")
        city = data.pop("city")
        foundation_year = data.pop("foundation_year")
        phone = data.pop("phone")

        if shop_name:
            about_me = data.pop("about_me")
            gender = data.pop("gender")
            age = data.pop("age")
            res_city = data.pop("residence_city")
            hair_type = data.pop("hair_type")
            phone_customer = data.pop("phone_customer")
            print(data)

        user_created = CustomUser.objects.create_user(data.pop("username"), data.pop("email"), data.pop("password"), **data)
        if data.get("type") == CustomUser.USER_TYPE_BARBER:
            BarberShop.objects.create(barber=user_created, name=shop_name, introduction=introduction, city=city, address=address, foundation_year=foundation_year, phone=phone)
        return user_created
