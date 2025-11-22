from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from recipes.models import Recipe
from recipes.forms import RecipeForm

class EditRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'edit_recipe.html'
    pk_url_kwarg = 'recipe_id'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        recipe = self.get_object()
        if recipe.user != request.user:
            return HttpResponseForbidden("You can not edit this recipe.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save()
        return redirect('get_recipe', self.object.id)