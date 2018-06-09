from django.contrib import admin
from bot.models import Item
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", "size", "category", "status", "updated_at")
    list_filter = ("status", "size", ("updated_at", DateTimeRangeFilter))
    search_fields = ("item_code",)


admin.site.register(Item, ItemAdmin)
