from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Recipe
from ..models import Comment
from ..forms import CommentForm
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect

import datetime

@login_required
def get_recipe(request, recipe_id):
    
    if request.method == "POST" and (request.POST.get('form_type') == 'comment_form'):
        form = CommentForm(request.POST)
        create_comment(request, recipe_id, form)
        path = reverse('get_recipe', kwargs={"recipe_id": f"{recipe_id}"}) 
        return HttpResponseRedirect(path)

    elif request.method == "POST" and (request.POST.get('form_type') == 'delete_comment_form'):
        delete_comment(request, recipe_id)
        path = reverse('get_recipe', kwargs={"recipe_id": f"{recipe_id}"}) 
        return HttpResponseRedirect(path)
    

    form = CommentForm()

    try:
        recipe =  Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Book not found.")

    comments = Comment.objects.all()

    context = {
    'recipe': recipe,
    'comments' : comments,
    'form' : form,
    }
    return render(request, "specific_recipe.html", context)


@login_required
def create_comment(request, recipe_id, form):
    if form.is_valid():
        try:
            comment_text = form.cleaned_data['comment']
            comment = Comment(user=request.user, recipe=Recipe.objects.get(pk=recipe_id), comment=comment_text, date_published=datetime.datetime.now())   
            comment.save()
        except:
            form.add_error(None, "Couldn't create this comment.")

           
@login_required
def delete_comment(request, recipe_id):

    try:
        comment_id = request.POST.get('comment_clicked')
        comment = Comment.objects.get(pk=comment_id)
    except:
        raise Http404(f"Could not delete comment")
        return HttpResponseNotFound()
    else: 
        comment.delete()



