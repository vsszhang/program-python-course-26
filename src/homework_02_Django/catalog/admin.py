from django.contrib import admin

from .models import Brand, Category, Tag, Watch, WatchDetail

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Watch)
admin.site.register(WatchDetail)
