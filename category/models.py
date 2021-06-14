from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.CharField(max_length=100, choices=( ('ອາຫານ', 'ອາຫານ'), ('ເຄື່ອງດື່ມ', 'ເຄື່ອງດື່ມ'), ('ສະຖານທີ່', 'ສະຖານທີ່') ))

    def __str__(self):
        return self.name
