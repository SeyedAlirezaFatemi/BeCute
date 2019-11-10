from django import forms
from customer.models import CustomUser


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'type',
        )

    def save(self, commit=True):
        data = self.cleaned_data
        user = CustomUser.objects.create_user(**data)
        return user
