from django.contrib import admin
from bot.models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", "size", "category", "status")
    list_filter = ("status", "size")
    search_fields = ("item_code",)


admin.site.register(Item, ItemAdmin)
