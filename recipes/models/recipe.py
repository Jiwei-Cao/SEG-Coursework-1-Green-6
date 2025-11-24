from django.db import models
from .user import User
from .tag import Tag

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_created')
    title = models.CharField(max_length=100)
    description = models.TextField()
    method = models.TextField()
    img = models.ImageField(upload_to='images/', blank=True, default='images/default.webp')
    tags = models.ManyToManyField(Tag,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favourites = models.ManyToManyField(User,blank=True, related_name='recipes_favourited')

    @property
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0

    @property
    def rating_count(self):
        return self.rating_set.count()

    def __str__(self):
        return self.title 