from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe, Ingredient, Unit, RecipeIngredient, UserIngredient

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)
admin.site.register(UserIngredient)