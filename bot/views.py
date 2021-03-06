import csv, datetime, json
from django.http import HttpResponseRedirect, HttpResponse
from bot.tasks import run
from bot.models import Item, Task
from django.shortcuts import render
from django.conf import settings


def process(request, *args, **kwargs):
    message = "Bot has been notified. Monitor the bot for details"
    trigger = request.GET.get("trigger")

    if trigger == "all":
        # Check for Available
        items = Item.objects.filter(status="available").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start+settings.BATCH_SIZE]
            if not len(temp):
                break
            start = start + settings.BATCH_SIZE
            t = Task.objects.create(completed_items=json.dumps([]), item_codes=str(temp), check_in_stock=False, status="new")
            run.delay(t.id)

        # Check for out of stock
        items = Item.objects.filter(status="out_of_stock").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start + settings.BATCH_SIZE]
            if not len(temp):
                break
            start = start + settings.BATCH_SIZE
            t = Task.objects.create(completed_items=json.dumps([]), item_codes=str(temp), check_in_stock=True, status="new")
            run.delay(t.id)

    if trigger == "out_of_stock":
        items = Item.objects.filter(status="available").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start + settings.BATCH_SIZE]
            if not len(temp):
                break
            start = start + settings.BATCH_SIZE
            t = Task.objects.create(completed_items=json.dumps([]), item_codes=str(temp), check_in_stock=False, status="new")
            run.delay(t.id)

    if trigger == "back_in_stock":
        items = Item.objects.filter(status="out_of_stock").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start + settings.BATCH_SIZE]
            if not len(temp):
                break
            start = start + settings.BATCH_SIZE
            t = Task.objects.create(completed_items=json.dumps([]), item_codes=str(temp), check_in_stock=True, status="new")
            run.delay(t.id)

    return render(request, 'index.html', {
        "total": Item.objects.count(),
        "available": Item.objects.filter(status="available").count(),
        "out_of_stock": Item.objects.filter(status="out_of_stock").count(),
        "removed": Item.objects.filter(status="removed").count(),
        "categories": Item.objects.values_list("category", flat=True).distinct(),
        "message": message
    })


def csv_download(request, *args, **kwargs):
    filename = None
    query_data = None
    if request.GET.get("type") == "available":
        filename = "available.csv"
        # Download all except removed items
        query_data = Item.objects.exclude(status="removed").values("item_code", "quantity", "size")
    if request.GET.get("type") == "out_of_stock":
        filename = "out_of_stock.csv"
        query_data = Item.objects.filter(status="out_of_stock").values("item_code", "quantity", "size", "status", "updated_at")
    if request.GET.get("type") == "back_in_stock_today":
        filename = "back_in_stock_today.csv"
        query_data = Item.objects.filter(status="available").values("item_code", "quantity", "size", "status", "updated_at")
        t = datetime.date.today()
        query_data = query_data.filter(updated_at__gt=datetime.datetime.fromordinal(t.toordinal()))
    if request.GET.get("type") == "out_of_stock_today":
        filename = "out_of_stock_today.csv"
        query_data = Item.objects.filter(status="out_of_stock").values("item_code", "quantity", "size", "status", "updated_at")
        t = datetime.date.today()
        query_data = query_data.filter(updated_at__gt=datetime.datetime.fromordinal(t.toordinal()))
    if request.GET.get("type") == "removed":
        filename = "removed.csv"
        query_data = Item.objects.filter(status="removed").values("item_code", "size", "status", "updated_at")

    print(filename)
    if filename not in ["available.csv", "out_of_stock.csv", "back_in_stock_today.csv", "removed.csv", "out_of_stock_today.csv"]:
        return render(request, 'index.html', {
            "total": Item.objects.count(),
            "available": Item.objects.filter(status="available").count(),
            "out_of_stock": Item.objects.filter(status="out_of_stock").count(),
            "removed": Item.objects.filter(status="removed").count(),
        })

    fp = open("/tmp/{}".format(filename), "w")
    writer = csv.writer(fp)
    writer.writerow(['Product SKU', 'quantity'])
    rows = []
    for data in query_data:
        rows.append(["{}{}".format(data.get('item_code'),data.get('size')), data.get('quantity')])
    writer.writerows(rows)
    fp.close()

    with open('/tmp/{}'.format(filename), 'rb') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response


def index(request, *args, **kwargs):
    return render(request, 'index.html', {
        "total": Item.objects.count(),
        "available": Item.objects.filter(status="available").count(),
        "out_of_stock": Item.objects.filter(status="out_of_stock").count(),
        "removed": Item.objects.filter(status="removed").count(),
    })


def retry(request, *args, **kwargs):
    run.delay(request.GET.get("task_id"))
    return HttpResponseRedirect("/admin/")


def retry_all(request, *args, **kwargs):
    for task in Task.objects.filter(status="failed"):
        run.delay(task.id)
    return HttpResponseRedirect("/")
