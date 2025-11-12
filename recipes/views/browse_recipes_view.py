from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def browse_recipes(request):
    return render(request, 'browse_recipes.html')
