from django.contrib import admin
from .models import Store, Staff, Modality, Booking, Patient

admin.site.register(Store)
admin.site.register(Staff)
admin.site.register(Modality)
admin.site.register(Booking)
admin.site.register(Patient)