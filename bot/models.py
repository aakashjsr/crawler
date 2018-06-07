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

    def __str__(self):
        return "{} - {}".format(self.item_code, self.size)
