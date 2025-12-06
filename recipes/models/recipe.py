from django.db import models
from .user import User
from .tag import Tag
from .comment import Comment
from .method_step import MethodStep

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_created')
    title = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to='images/', blank=True, null=True,default='images/default.webp')
    tags = models.ManyToManyField(Tag,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favourites = models.ManyToManyField(User,blank=True, related_name='recipes_favourited')
    public = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name='recipe_comments')
    method_steps = models.ManyToManyField(MethodStep, blank=True, related_name='recipe_method_steps')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_tags()

    @property
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0

    @property
    def rating_count(self):
        return self.rating_set.count()
    
    def update_tags(self):
        allergens = [
            {
            "category": "NT",
            "tag_name": "Nut-free"
            },
            {
            "category": "DR",
            "tag_name": "Dairy-free"
            },
            {
            "category": "GL",
            "tag_name": "Gluten-free"
            },
            {
            "category": "BT",
            "tag_name": "Vegetarian"
            }
        ]
        ingredients = self.recipeingredient_set.all()
        for allergen in allergens:
            contains_ingredient = ingredients.filter(ingredient__category=allergen["category"]).exists()
            tag, create= Tag.objects.get_or_create(name=allergen["tag_name"])
            if contains_ingredient:
                self.tags.remove(tag)
            else:
                self.tags.add(tag)


    def __str__(self):
        return self.title