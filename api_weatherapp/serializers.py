from rest_framework import serializers

from sofia_weather.models import SubscribedUsers


class SubscribedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUsers
        fields = '__all__'