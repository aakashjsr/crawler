from django.db import models


class Item(models.Model):
    item_code = models.CharField(max_length=25)
    size = models.CharField(max_length=25)
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
    ended_at = models.DateTimeField(null=True, blank=True)
    execution_time = models.CharField(max_length=25, null=True)
    item_codes = models.CharField(max_length=5000)
    check_in_stock = models.BooleanField(default=False)
    exception_message = models.TextField(max_length=5000)

    def __str__(self):
        return "{} - {}".format(self.id, self.percent)