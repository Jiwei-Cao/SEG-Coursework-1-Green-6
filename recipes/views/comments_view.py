from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Recipe, Comment
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
import datetime
from django.urls import reverse

@login_required
def handle_comments(request, recipe_id):
	recipe = get_object_or_404(Recipe, id=recipe_id)
	if validate_comment_request(request):
		create_comment(request, recipe)
	elif is_delete_comment_post(request):
		delete_comment(request, recipe)

	path = reverse('get_recipe', kwargs={"recipe_id": f"{recipe_id}"}) 
	return HttpResponseRedirect(path)


def is_create_comment_post(request):
    return request.method == "POST" and request.POST.get("form_type") == "comment_form"


def validate_comment_request(request):
	comment_text = request.POST.get('comment_text', '')
	if (comment_text == '') or (len(comment_text) > 500):
		return False
	else:
		return True 


def create_comment(request, recipe):
    try:
        comment = Comment(user=request.user, comment=request.POST.get('comment_text'), date_published=datetime.datetime.now())
        comment.save()
        recipe.comments.add(comment)
    except:
    	raise Http404(f"Could not create comment")
    	return HttpResponseNotFound()


def is_delete_comment_post(request):
    return request.method == "POST" and request.POST.get("form_type") == "delete_comment_form"

def delete_comment(request, recipe):
    try:
    	comment = Comment.objects.get(pk=request.POST.get('comment_clicked'))
    	recipe.comments.remove(comment)
    except:
        raise Http404(f"Could not delete comment")
        return HttpResponseNotFound()
    else: 
        comment.delete()