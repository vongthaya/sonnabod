from django.db import models


class DiscountType(models.Model):
    short_name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.short_name