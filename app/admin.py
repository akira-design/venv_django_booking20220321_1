from django.contrib import admin
from .models import Store, Staff, Modality, Booking, Patient, ParentCategory, Category, Remark

admin.site.register(Store)
admin.site.register(Staff)
admin.site.register(Modality)
admin.site.register(Booking)
admin.site.register(Patient)
# admin.site.register(Post)
admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(Remark)