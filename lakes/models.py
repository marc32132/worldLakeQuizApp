from django.db import models


class Lake(models.Model):
    name = models.CharField("name", max_length=255)
    country = models.CharField("country", max_length=255)

    def __str__(self):
        return self.name