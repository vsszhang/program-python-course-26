from django.contrib import admin

from .models import Brand, Category, Tag, Watch, WatchDetail


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "founded_year")
    search_fields = ("name", "country")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class WatchDetailInline(admin.StackedInline):
    model = WatchDetail
    extra = 0


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "movement_type",
        "price",
        "purchase_date",
        "is_in_collection",
    )
    list_filter = ("brand", "category", "movement_type", "is_in_collection")
    # `brand__name` is a ralationship search: from BRAND field to NAME field, like SQL
    search_fields = ("name", "brand__name", "description")
    filter_horizontal = ("tags",)
    inlines = [WatchDetailInline]


@admin.register(WatchDetail)
class WatchDetailAdmin(admin.ModelAdmin):
    list_display = (
        "watch",
        "case_size",
        "case_material",
        "water_resistance",
        "lug_width",
        "has_date",
    )
