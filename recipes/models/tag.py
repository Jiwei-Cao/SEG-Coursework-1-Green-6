from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100,unique=True)
    colour = models.CharField(
        max_length=7,
        default="#61D0FF"
    )
    def __str__(self):
        return self.name