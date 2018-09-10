from django.db import models


FILTER_TYPE = (
    ('INT', 'INT'),
    ('BOOL', 'BOOL'),
    ('FLOAT', 'FLOAT'),
    ('STRING', 'STRING'),
)


class Filter(models.Model):
    name = models.CharField(max_length=200, null=False, verbose_name="Name", )
    type = models.CharField(max_length=10, choices=FILTER_TYPE, default='INT', null=False, verbose_name="Type", )
    description = models.CharField(max_length=200, null=False, verbose_name="Description", )

    def __str__(self):
        return self.name
