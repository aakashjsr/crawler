from django.contrib import admin
from bot.models import Item, Task
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", "size", "category", "status", "updated_at")
    list_filter = ("status", "size", ("updated_at", DateTimeRangeFilter))
    search_fields = ("item_code",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "started_at", "check_in_stock", "percent", "status")
    list_filter = ("status", ("started_at", DateTimeRangeFilter))


admin.site.register(Item, ItemAdmin)
admin.site.register(Task, TaskAdmin)
