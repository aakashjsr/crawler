from bot.models import Item
import csv

fp = open("products_export.csv")
readCSV = csv.reader(fp)

# readCSV.next()

items_list = []
for row in readCSV:
    try:
        if row[2].index('<td>XS </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xs"))
    except:
        pass
    try:
        if row[2].index('<td>s </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="s"))
    except:
        pass
    try:
        if row[2].index('<td>m </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="m"))
    except:
        pass
    try:
        if row[2].index('<td>l </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="l"))
    except:
        pass
    try:
        if row[2].index('<td>xl </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xl"))
    except:
        pass
    try:
        if row[2].index('<td>xxl </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xxl"))
    except:
        pass
    try:
        if row[2].index('<td>xxxl </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xxxl"))
    except:
        pass
    try:
        if row[2].index('<td>xxxxl </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xxxxl"))
    except:
        pass
    try:
        if row[2].index('<td>xxxxxl </td>'):
            items_list.append(Item(item_code=row[0], status="available", size="xxxxxl"))
    except:
        pass

Item.objects.all().delete()
Item.objects.bulk_create(items_list)
