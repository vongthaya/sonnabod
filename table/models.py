from django.db import models

class Table(models.Model):
    number = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.number