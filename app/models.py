from django.contrib.auth.models import AbstractUser
from django.db import models

class AppUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    email = models.EmailField(null=True, default=None)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class GlobalUserdata(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    spam_likely_hood = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class ContactList(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SpamReport(models.Model):
    phone_number = models.CharField(max_length=15)
    reporter = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    report_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('phone_number', 'reporter')

    def __str__(self):
        return self.reporter.username
