from django import forms

from sofia_weather.core.forms import BootstrapFormMixin
from sofia_weather.models import SubscribedUsers


class SubscribedUsersForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email here',
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            SubscribedUsers.objects.get(email=email)

        except SubscribedUsers.DoesNotExist:
            return email

        raise forms.ValidationError('This email already exists!')

    def send_email(self):
        pass
