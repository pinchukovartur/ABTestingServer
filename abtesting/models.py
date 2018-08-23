from django.db import models


class Filter(models.Model):
    name = models.CharField(max_length=200, null=False, verbose_name="Name", )

    def __str__(self):
        return self.name
