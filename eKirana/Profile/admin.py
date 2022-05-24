from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)


# @admin.register(Profile)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['id','first_name','last_name','marks','city']