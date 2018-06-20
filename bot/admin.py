from django.contrib import admin
from bot.models import Item, Task, ProductList
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", "size", "category", "status", "updated_at")
    list_filter = ("status", "size", "category", ("updated_at", DateTimeRangeFilter))
    search_fields = ("item_code",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "started_at", "ended_at", "execution_time", "check_in_stock", "percent", "status")
    list_filter = ("status", ("started_at", DateTimeRangeFilter))


class ProductListkAdmin(admin.ModelAdmin):
    list_display = ("uploaded_on", "file_link")


admin.site.register(Item, ItemAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ProductList, ProductListkAdmin)
