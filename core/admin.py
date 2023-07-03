from django.contrib import admin

from core.models import Transaction, Currency, Catagory

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Currency)
admin.site.register(Catagory)
