import csv


def get_sizes(body):
    size_list = []
    try:
        if body.index('<td>XS </td>'):
            size_list.append("xs")
    except:
        pass
    try:
        if body.index('<td>S </td>'):
            size_list.append("s")
    except:
        pass
    try:
        if body.index('<td>M </td>'):
            size_list.append("m")
    except:
        pass
    try:
        if body.index('<td>L </td>'):
            size_list.append("l")
    except:
        pass
    try:
        if body.index('<td>XL </td>'):
            size_list.append("xl")
    except:
        pass
    try:
        if body.index('<td>XXL </td>'):
            size_list.append("xxl")
    except:
        pass
    try:
        if body.index('<td>XXXL </td>'):
            size_list.append("xxxl")
    except:
        pass
    try:
        if body.index('<td>XXXXL </td>'):
            size_list.append("xxxxl")
    except:
        pass
    try:
        if body.index('<td>XXXXXL </td>'):
            size_list.append("xxxxxl")
    except:
        pass
    return size_list


def process_csv(path):
    from bot.models import Item
    item_list = []
    item_hash = {}
    for item in Item.objects.all():
        if not item_hash.get(item.item_code):
            item_hash[item.item_code] = []
        item_hash[item.item_code].append(item.size)

    fp = open(path, encoding='utf-8')
    reader = csv.DictReader(fp)
    data = [i for i in reader]
    data.pop(0)

    for row in data:
        code = row.get("Handle", '').lower()
        category = row.get("Type", '').lower()
        body = row.get("Body (HTML)", '')
        sizes = get_sizes(body)
        for size in sizes:
            if item_hash.get(code) and (size in item_hash.get(code)):
                pass
            else:
                item_list.append(Item(item_code=code, size=size, category=category, status="available"))

    Item.objects.bulk_create(item_list)
    print("Created {} items.".format(len(item_list)))

    fp.close()
