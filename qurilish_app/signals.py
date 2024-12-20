from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from qurilish_proj import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Your Website Title"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "noreply@yourdomain.com",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    mail = send_mail(
        subject="Password Reset for {title}".format(title="Your Website Title"),
        message=email_plaintext_message,
        html_message=email_html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[reset_password_token.user.email],
        fail_silently=True
    )
    # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()
