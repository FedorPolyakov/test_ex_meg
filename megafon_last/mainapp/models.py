from django.db import models
from django.utils import timezone


class PostNumber(models.Model):
    number_int = models.CharField(max_length=50)
    number_str = models.TextField(blank=True)
    nds = models.BooleanField(blank=True)
    nds_percent = models.IntegerField(default=0, blank=True, null=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.number_int

    def publish(self):
        self.save()
