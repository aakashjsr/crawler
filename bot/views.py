from django.http import HttpResponse
from bot.tasks import run
from bot.models import Item
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
            run.delay(temp, False)

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
            run.delay(temp, False)

    if trigger == "back_in_stock":
        items = Item.objects.filter(status="out_of_stock").values_list('item_code', flat=True)
        items = list(set(items))
        start = 0
        while True:
            temp = items[start: start + 100]
            if not len(temp):
                break
            start = start + 100
            run.delay(temp, True)

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
