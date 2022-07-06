from django import forms

from sofia_weather.core.forms import BootstrapFormMixin
from sofia_weather.models import SubscribedUsers
from celery_utils.tasks import send_email_after_subscription_task


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
        send_email_after_subscription_task.delay(self.email, self.name)
