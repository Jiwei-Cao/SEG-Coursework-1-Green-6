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
    EGG = "EG"
    DAIRY = "DR"
    NUT = "NT"
    GLUTEN = "GL"
    ALCOHOL = "AL"
    FRUIT = "FR"
    PULSES = "PS"
    GRAINS = "GR"
    WATER = "WT"
    ALLUM = "AL"
    MINERALS = "ML"
    CHOICES = ()
    CATEGORY_OPTIONS = {
        NONE: "None",
        VEGETABLE: "Vegetable",
        SPICE: "Spice",
        HERBS: "Herbs",
        BUTCHERY: "Butchery",
        SEAFOOD: "Seafood",
        EGG: "Egg",
        DAIRY: "Dairy",
        NUT: "Nut",
        GLUTEN: "Gluten",
        ALCOHOL: "Alcohol",
        FRUIT: "Fruit",
        PULSES: "Pulses",
        GRAINS: "Grains",
        WATER: "Water",
        ALLUM: "Allum",
        MINERALS: "Minerals",
    }
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_OPTIONS,
        default=NONE
    )
    quantity = models.DecimalField(decimal_places=2, max_digits= 10)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity) +  " " + str(self.unit) + " of " + self.name