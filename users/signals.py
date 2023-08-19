from django.contrib.auth.models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    # print('Profile Saved!')
    # print('Instance: ', instance)
    # print('CREATED: ', created)
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        send_mail(
            'Welcome to DevSearch',
            'We are glod you are here!',
            settings.EMAIL_HOST_USER,
            [profile.email, 'mohammad_naderinasab@yahoo.com'],
            fail_silently=False
        )

# @receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# @receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    # print('Profile Successfully Deleted!')
    # print('Instance: ', instance)
    # print('CREATED: ', sender)
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)