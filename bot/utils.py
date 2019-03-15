import csv


def get_sizes(body):
    size_list = []
    try:
        if body.index('<td>XS </td>'):
            size_list.append("XS")
    except:
        pass
    try:
        if body.index('<td>S </td>'):
            size_list.append("S")
    except:
        pass
    try:
        if body.index('<td>M </td>'):
            size_list.append("M")
    except:
        pass
    try:
        if body.index('<td>L </td>'):
            size_list.append("L")
    except:
        pass
    try:
        if body.index('<td>XL </td>'):
            size_list.append("XL")
    except:
        pass
    try:
        if body.index('<td>XXL </td>'):
            size_list.append("XXL")
    except:
        pass
    try:
        if body.index('<td>XXXL </td>'):
            size_list.append("XXXL")
    except:
        pass
    try:
        if body.index('<td>XXXXL </td>'):
            size_list.append("XXXXL")
    except:
        pass
    try:
        if body.index('<td>XXXXXL </td>'):
            size_list.append("XXXXXL")
    except:
        pass
    try:
        if body.index('<td>XXXXXXL </td>'):
            size_list.append("XXXXXXL")
    except:
        pass
    return size_list


def get_data_from_stream(fp, data):
    """
    Handles corrupted file streams
    """
    reader = csv.DictReader(fp)
    try:
        for i in reader:
            data.append(i)
    except:
        get_data_from_stream(fp, data)


def process_csv(path):
    from bot.models import Item
    item_list = []
    item_hash = {}
    for item in Item.objects.all():
        if not item_hash.get(item.item_code):
            item_hash[item.item_code] = []
        item_hash[item.item_code].append(item.size)

    fp = open(path, encoding='utf-8')
    data = []
    get_data_from_stream(fp, data)
    data.pop(0)

    for row in data:
        try:
            code = row["Handle"].lower()
        except:
            print("No Code . Skipping")
            continue
        category = row.get("Type", '').lower()
        try:
            size = row.get("Option2 Value").strip().split(")")[-1]
            if not size:
                print("No Size")
                continue
        except:
            print("No Size. Skipping")
            continue
        if item_hash.get(code) and (size in item_hash.get(code)):
            pass
        else:
            item_list.append(Item(item_code=code, size=size, category=category, status="available"))

    Item.objects.bulk_create(item_list)
    print("Created {} items.".format(len(item_list)))

    fp.close()
