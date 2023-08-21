from django.contrib import admin
from .models import AppUser, GlobalUserdata, ContactList, SpamReport

admin.site.register(AppUser)
admin.site.register(GlobalUserdata)
admin.site.register(ContactList)
admin.site.register(SpamReport)