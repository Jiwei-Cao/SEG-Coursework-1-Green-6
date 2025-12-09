from django.db import models
from .user import User
from django.core.validators import MinValueValidator, MaxValueValidator

class MethodStep(models.Model):
    '''Model used for creating method steps'''
    step_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    method_text = models.TextField(blank=False, max_length=256)
    
    class Meta:
        '''Orders based on step number, in ascending order'''
        ordering = ('step_number',)
