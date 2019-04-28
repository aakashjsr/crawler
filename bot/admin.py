from django.contrib import admin
from bot.models import Item, Task, ProductList
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", "size", "quantity", "status")
    fields = ("item_code", "size", "quantity")
    readonly_fields = ("updated_at", )
    search_fields = ("item_code",)
    list_filter = ("status", )


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "started_at", "ended_at", "execution_time", "check_in_stock", "percent", "status")
    list_filter = ("status", ("started_at", DateTimeRangeFilter))


class ProductListkAdmin(admin.ModelAdmin):
    list_display = ("uploaded_on", "file_link")


admin.site.register(Item, ItemAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ProductList, ProductListkAdmin)
