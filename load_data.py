import json
from bot.models import Item

f = open("data.txt")
data = f.read()
f.close()
data = json.loads(data)

item_list = []
for i in data:
    item_list.append(Item(**i))

Item.objects.all().delete()
Item.objects.bulk_create(item_list)