from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email_after_subscription(email, name):
    context = {
        'name': name,
        'email': email
    }
    email_subject = 'Thank you for subscription'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email, ]
    )
    return email.send(fail_silently=False)