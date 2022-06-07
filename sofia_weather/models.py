from django.db import models


class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Subscribed Users'

    def __str__(self):
        return self.email
