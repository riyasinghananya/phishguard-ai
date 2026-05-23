from django.db import models

class Scan(models.Model):

    url = models.URLField()

    result = models.CharField(max_length=100)

    def _str_(self):
        return self.url
# Create your models here.
