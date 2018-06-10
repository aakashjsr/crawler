from django.db import models


class Item(models.Model):
    item_code = models.CharField(max_length=25)
    size = models.CharField(max_length=25, choices=[
        ("s", "s"), ("m", "m"), ("l", "l"), ("xl", "xl"), ("xxl", "xxl")
    ])
    category = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=15, choices=[
        ("available", "available"), ("out_of_stock", "out_of_stock"), ("removed", "removed")
    ])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.item_code, self.size)


class Task(models.Model):
    percent = models.IntegerField(default=0)
    status = models.CharField(max_length=25)
    started_at = models.DateTimeField(auto_now_add=True)
    item_codes = models.CharField(max_length=5000)
    check_in_stock = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.id, self.percent)