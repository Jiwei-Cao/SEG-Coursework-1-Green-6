from django.db import models
from .user import User

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    NONE = "NN"
    VEGETABLE = "VG"
    SPICE = "SP"
    HERBS = "HB"
    BUTCHERY = "BT"
    SEAFOOD = "SF"
    CATEGORY_OPTIONS = {
        NONE: "None",
        VEGETABLE: "Vegetable",
        SPICE: "Spice",
        HERBS: "Herbs",
        BUTCHERY: "Butchery",
        SEAFOOD: "Seafood"
    }
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_OPTIONS,
        default=NONE
    )

    def __str__(self):
        return self.name 