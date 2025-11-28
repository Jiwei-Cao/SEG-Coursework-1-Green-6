from django.db import models
from .user import User
from django.core.validators import MinValueValidator, MaxValueValidator

class MethodStep(models.Model):
    step_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    method_text = models.TextField(blank=False, max_length="256")
    
    class Meta:
        ordering = ('step_number',)
