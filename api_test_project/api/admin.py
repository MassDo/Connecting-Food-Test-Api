from django.contrib import admin

from .models import Certificate, Farmer, Product

admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Certificate)
