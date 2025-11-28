from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from recipes.models import UserIngredient

@login_required
@require_POST
def delete_ingredient(request, ingredient_pk):
    current_user = request.user
    ingredient = get_object_or_404(UserIngredient, id=ingredient_pk)
    if current_user == ingredient.user:
        ingredient.delete()
        return HttpResponseRedirect(reverse('cupboard'))
    return HttpResponseForbidden("You are not allowed to delete this ingredient.")