from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member, Invite, User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import threading
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

@receiver(post_save, sender=Member)
def delete_duplicate_members(sender, instance, **kwargs):
    if instance.acceptance_status:
        Member.objects.filter(user=instance.user).exclude(pk=instance.pk).delete()

@receiver(post_save, sender=Invite)
def send_invite_email(sender, instance, created, **kwargs):
    email_thread = threading.Thread(target=send_mail_func,kwargs=({'sender': sender, 'instance': instance, 'created': created}))
    email_thread.start()

@receiver(post_save, sender=User)
def send_confirm_email(sender, instance, created, **kwargs):
    email_thread = threading.Thread(target=send_verification_email,kwargs=({'user': instance, 'created': created}))
    email_thread.start()
    
def send_mail_func(sender, instance, created, **kwargs):
    print("send_invite_email signal called")
    
    if created:
        subject = 'Team-Invitation'
        recipient_list = [instance.receiver.user.email]
        image_url = f'http://{settings.DOMAIN}/static/assets/img/banner.png'
        invite_url = f'http://{settings.DOMAIN}/profile/request/'
        html_message = render_to_string('invite_email_template.html', {'sender_name': f'{instance.sender.user.first_name} {instance.sender.user.last_name}','user':instance.receiver.user.first_name, 'image_url':image_url, 'invite_url':invite_url})

        send_mail(subject, '', 'codeshackcommunity@gmail.com', recipient_list, html_message=html_message)
        
def send_verification_email(user, created):
    print("send_confirm_email signal called")
    if created:
        token = default_token_generator.make_token(user)
        uid = user.pk
        verification_url = f"http://{settings.DOMAIN}/user/verify-email/{uid}:{token}/"
        subject = 'Email Verification'
        recipient_list = [user.email]
        print(verification_url)
        html_message = render_to_string('email_confirm_template', {'verification_url': verification_url})
        
        send_mail(subject, '', 'codeshackcommunity@gmail.com', recipient_list, html_message=html_message)