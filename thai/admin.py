from django.contrib import admin

# Register your models here.
from .models import Province, District, SubDistrict

admin.site.register(Province)
admin.site.register(District)
admin.site.register(SubDistrict)
