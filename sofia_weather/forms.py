from django import forms

from sofia_weather.core.forms import BootstrapFormMixin
from sofia_weather.models import SubscribedUsers


class SubscribedUsersForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = '__all__'

    def send_email(self):
        pass
