import json
from bot.tasks import run
from bot.models import Item, Task
from django.shortcuts import render


def process(request, *args, **kwargs):
    message = "Bot has been notified. Monitor the bot for details"
    trigger = request.GET.get("trigger")

    if trigger == "all":
        items = Item.objects.filter(status="available").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start+100]
            if not len(temp):
                break
            start = start + 100
            t = Task.objects.create(item_codes=json.dumps(temp), check_in_stock=False, status="new")
            run.delay(t.id)

    if trigger == "category":
        items = Item.objects.filter(
            status="available", category=request.GET.get("category")
        ).values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start+100]
            if not len(temp):
                break
            start = start + 100
            t = Task.objects.create(item_codes=json.dumps(temp), check_in_stock=False, status="new")
            run.delay(t.id)

    if trigger == "back_in_stock":
        items = Item.objects.filter(status="out_of_stock").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start + 100]
            if not len(temp):
                break
            start = start + 100
            t = Task.objects.create(item_codes=json.dumps(temp), check_in_stock=True, status="new")
            run.delay(t.id)

    return render(request, 'index.html', {
        "total": Item.objects.count(),
        "available": Item.objects.filter(status="available").count(),
        "out_of_stock": Item.objects.filter(status="out_of_stock").count(),
        "removed": Item.objects.filter(status="removed").count(),
        "categories": Item.objects.values_list("category", flat=True).distinct(),
        "message": message
    })


def index(request, *args, **kwargs):
    return render(request, 'index.html', {
        "total": Item.objects.count(),
        "available": Item.objects.filter(status="available").count(),
        "out_of_stock": Item.objects.filter(status="out_of_stock").count(),
        "removed": Item.objects.filter(status="removed").count(),
        "categories": Item.objects.values_list("category", flat=True).distinct()
    })
