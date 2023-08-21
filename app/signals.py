from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SpamReport, GlobalUserdata
from django.db.models import F

@receiver(post_save, sender=SpamReport)
def update_books_on_author_save(sender, instance, created, **kwargs):
    if created:
        GlobalUserdata.objects.filter(phone_number=instance.phone_number).update(spam_likely_hood = F('spam_likely_hood')+1)