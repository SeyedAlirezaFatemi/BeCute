from django import forms

from customer.models import Comment


class CommentForm(forms.ModelForm):
    rate = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Comment
        fields = ['content', 'rate']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.barbershop = kwargs.pop("barbershop")
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        data = self.cleaned_data
        rate = data.pop("rate")
        content = data.pop("content")
        user = self.request.user
        barbershop = self.barbershop
        comment_created = Comment(rate=rate, customer=user, content=content, barbershop=barbershop)
        comment_created.save()
        return comment_created
