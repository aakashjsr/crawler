import time
from django.http import HttpResponse
from bot.tasks import run
from bot.models import Item


def test(request, *args, **kwargs):
    s_t = time.time()
    items = Item.objects.filter(status="available").values_list('item_code', flat=True)
    items = list(set(items))
    start = 0
    # run.delay(["LC61847-2"])
    while True:
        temp = items[start: start+100]
        if not len(temp):
            break
        start = start + 100
        # print(temp)
        run.delay(temp)
    e_t = time.time()
    return HttpResponse("Splitting took {} ms".format((e_t-s_t)*1000))
