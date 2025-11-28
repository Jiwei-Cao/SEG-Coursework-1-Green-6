from django.db import models
from .user import User
from .unit import Unit

class UserIngredient(models.Model):
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
    quantity = models.DecimalField(decimal_places=2, max_digits= 10)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity) + str(self.unit) + " of " + self.name