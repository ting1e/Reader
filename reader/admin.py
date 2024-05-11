from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(BookGroup)
admin.site.register(UserBookRecord)
admin.site.register(UserSetting)
admin.site.register(UserBookMark)
