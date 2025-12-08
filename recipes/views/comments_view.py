from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Recipe, Comment
from ..forms import CommentForm

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound

import datetime
from django.utils.timezone import make_aware

from django.urls import reverse

@login_required
def handle_add_comment(request, recipe_id):
	'''Call method to create a comment and redirect user to recipe it belongs to'''
	recipe = get_object_or_404(Recipe, id=recipe_id)
	handle_create_comment_post(request, recipe)
	return redirect_to_specific_recipe_page(recipe_id)


def handle_create_comment_post(request, recipe):
	'''Check form is valid before creating a comment on a recipe'''
	form = CommentForm(request.POST)
	if(form.is_valid()):
		create_comment(request, recipe, form)

def create_comment(request, recipe, form):
	'''Create comment object and save it to the database'''
	try:
		comment = Comment(user=request.user, comment=form.cleaned_data['comment'], date_published=make_aware(datetime.datetime.now()))
		comment.save()
		recipe.comments.add(comment)
	except:
		raise Http404("Could not create comment")


@login_required
def handle_delete_comment(request, recipe_id, comment_id):
	''' Call method to delete comment and redirect user to the recipe it belonged to'''
	recipe = get_object_or_404(Recipe, id=recipe_id)
	delete_comment(request, recipe, comment_id)
	return redirect_to_specific_recipe_page(recipe_id)

def delete_comment(request, recipe, comment_id):
	'''Delete an individual comment object '''
	try:
		comment = Comment.objects.get(pk=comment_id)
	except:
		raise Http404(f"Could not delete comment")
	else: 
		recipe.comments.remove(comment)
		delete_comment_replies(comment)
		comment.delete()


def delete_comment_replies(comment):
	'''Delete all of the specified comment's replies'''
	for reply in comment.replies.all():
		reply.delete()



@login_required
def handle_add_reply_comment(request, recipe_id, parent_comment_id):
	''' Call method to create a reply comment '''
	parent_comment = get_object_or_404(Comment, id=parent_comment_id)
	handle_create_reply_post(request, parent_comment)
	return redirect_to_specific_recipe_page(recipe_id)


def handle_create_reply_post(request, parent_comment):
	'''Check form is valid before creating reply comment'''
	form = CommentForm(request.POST)
	if(form.is_valid()):
		create_reply_comment(request, parent_comment, form)

def create_reply_comment(request, parent_comment, form):
	'''Create a reply comment and save it to it's parent comment object'''
	try:
		reply = Comment(user=request.user, comment=form.cleaned_data['comment'], date_published=make_aware(datetime.datetime.now()))
		reply.save()
		parent_comment.replies.add(reply)
		
	except:
		raise Http404(f"Could not create reply comment")



@login_required
def handle_delete_reply_comment(request, recipe_id, parent_comment_id, reply_comment_id):
	''' Call method to delete a reply comment '''
	recipe = get_object_or_404(Recipe, id=recipe_id)
	parent_comment = get_object_or_404(Comment, id=parent_comment_id)
	delete_reply_comment(request, parent_comment, reply_comment_id)
	return redirect_to_specific_recipe_page(recipe_id)
	


def delete_reply_comment(request, parent_comment, reply_comment_id):
	'''Delete a reply comment object'''
	try:
		reply = Comment.objects.get(pk=reply_comment_id)
		parent_comment.replies.remove(reply)
	except:
		raise Http404(f"Could not delete reply comment")

	else:
		reply.delete()


def redirect_to_specific_recipe_page(recipe_id):
	'''Redirect user to the specified recipe page'''
	path = reverse('get_recipe', kwargs={"recipe_id": f"{recipe_id}"}) 
	return HttpResponseRedirect(path)
