from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from math import floor
import datetime

from ..models import Recipe, Rating, Comment
from ..forms import CommentForm  # assuming your CommentForm is defined

@login_required
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "rating_form":
            handle_rating_post(request, recipe)
            return HttpResponseRedirect(request.path_info)

        elif form_type == "comment_form":
            form = CommentForm(request.POST)
            create_comment(request, recipe, form)
            return HttpResponseRedirect(request.path_info)

        elif form_type == "delete_comment_form":
            delete_comment(request)
            return HttpResponseRedirect(request.path_info)

    form = CommentForm()
    context = create_recipe_context(request.user, recipe)
    context["form"] = form
    context["comments"] = Comment.objects.filter(recipe=recipe).order_by("-date_published")
    return render(request, "specific_recipe.html", context)


def handle_rating_post(request, recipe):
    rating_value = request.POST.get("rating")
    if not rating_value:
        return
    try:
        rating_value = int(rating_value)
    except ValueError:
        return
    if 1 <= rating_value <= 5:
        Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={'rating': rating_value}
        )

def get_user_rating(user, recipe):
    rating = Rating.objects.filter(user=user, recipe=recipe).first()
    return rating.rating if rating else None

def calculate_star_distribution(average_rating):
    full_stars = int(floor(average_rating))
    half_star = 1 if average_rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return full_stars, half_star, empty_stars

def create_recipe_context(user, recipe):
    user_rating = get_user_rating(user, recipe)
    average_rating = recipe.average_rating or 0
    rating_count = recipe.rating_count or 0
    full_stars, half_star, empty_stars = calculate_star_distribution(average_rating)

    return {
        "recipe": recipe,
        "user_rating": user_rating,
        "average_rating": average_rating,
        "rating_count": rating_count,
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
    }


# ----- Comment helpers -----
@login_required
def create_comment(request, recipe, form):
    if form.is_valid():
        try:
            comment_text = form.cleaned_data['comment']
            Comment.objects.create(
                user=request.user,
                recipe=recipe,
                comment=comment_text,
                date_published=datetime.datetime.now()
            )
        except Exception:
            form.add_error(None, "Couldn't create this comment.")


@login_required
def delete_comment(request):
    try:
        comment_id = request.POST.get('comment_clicked')
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
    except Comment.DoesNotExist:
        raise Http404("Could not delete comment")
