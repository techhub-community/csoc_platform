from loguru import logger
import threading

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from .models import Member, Invite, User


@receiver(post_save, sender=Member)
def delete_duplicate_members(sender, instance, **kwargs):
    if instance.acceptance_status:
        logger.info(f"{instance.user} is not part of a {instance.team}, deleting all other relations")
        Member.objects.filter(user=instance.user).exclude(pk=instance.pk).delete()


@receiver(post_save, sender=Invite)
def send_invite_email(sender, instance, created, **kwargs):
    try:
        email_thread = threading.Thread(target=send_mail_func,kwargs=({'sender': sender, 'instance': instance, 'created': created}))
        email_thread.start()
    except Exception as e:
        logger.info(f"Failed to send mail to {instance.receiver}, sent by {sender}")


@receiver(post_save, sender=User)
def send_confirm_email(sender, instance, created, **kwargs):
    try:
        email_thread = threading.Thread(target=send_verification_email,kwargs=({'user': instance, 'created': created}))
        email_thread.start()
    except Exception as e:
        logger.info(f"Failed to send verification mail to {instance}")


def send_mail_func(sender, instance, created, **kwargs):
    if created:
        logger.info(f"sending invite for {instance.team} by {instance.sender} to {instance.receiver}")
        subject = 'Team-Invitation'
        recipient_list = [instance.receiver.user.email]
        image_url = f'https://{settings.DOMAIN}/static/assets/img/banner.png'
        invite_url = f'https://{settings.DOMAIN}/user/profile/'
        html_message = render_to_string('invite_email_template.html', {'sender_name': f'{instance.sender.user.first_name} {instance.sender.user.last_name}','user':instance.receiver.user.first_name, 'image_url':image_url, 'invite_url':invite_url})
        send_mail(subject, '', settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)


def send_verification_email(user, created):
    if created:
        logger.info(f"sending verification mail to {user}")
        token = default_token_generator.make_token(user)
        uid = user.pk
        pk=f"{uid}:{token}"
        verification_url = f"https://{settings.DOMAIN}/user/verify-email/{uid}:{token}/"
        logger.info(f"generated verification link: {verification_url}")
        subject = 'Email Verification'
        recipient_list = [user.email]
        print(verification_url)
        html_message = render_to_string('email_confirm_template.html', {'verification_url': verification_url})
        send_mail(subject, '', settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)