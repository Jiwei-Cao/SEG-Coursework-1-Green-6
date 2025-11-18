from django.db import models

class Tag(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name