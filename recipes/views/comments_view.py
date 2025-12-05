from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Recipe, Comment
from ..forms import CommentForm

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound

import datetime
from django.utils.timezone import make_aware

from django.urls import reverse

@login_required
def handle_comments(request, recipe_id):
	recipe = get_object_or_404(Recipe, id=recipe_id)
	if is_create_comment_post(request):
		handle_create_comment_post(request, recipe)
	elif is_delete_comment_post(request):
		delete_comment(request, recipe)
	elif is_reply_comment_post(request):
		handle_create_reply_post(request)
	elif is_delete_reply_comment_post(request):
		delete_reply_comment(request)


	path = reverse('get_recipe', kwargs={"recipe_id": f"{recipe_id}"}) 
	return HttpResponseRedirect(path)


def is_create_comment_post(request):
    return request.method == "POST" and request.POST.get("form_type") == "comment_form"

def handle_create_comment_post(request, recipe):
	form = CommentForm(request.POST)
	if(form.is_valid()):
		create_comment(request, recipe, form)

def create_comment(request, recipe, form):
	try:
		comment = Comment(user=request.user, comment=form.cleaned_data['comment'], date_published=make_aware(datetime.datetime.now()))
		comment.save()
		recipe.comments.add(comment)
	except:
		raise Http404("Could not create comment")
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

def is_reply_comment_post(request):
	return request.method == "POST" and request.POST.get("form_type") == "reply_comment_form"

def handle_create_reply_post(request):
	form = CommentForm(request.POST)
	if(form.is_valid()):
		create_reply_comment(request, form)

def create_reply_comment(request, form):
	try:
		reply = Comment(user=request.user, comment=form.cleaned_data['comment'], date_published=make_aware(datetime.datetime.now()))
		reply.save()
		parent_comment = Comment.objects.get(pk=request.POST.get('parent_comment'))
		parent_comment.replies.add(reply)
		
	except:
		raise Http404(f"Could not create reply comment")
		return HttpResponseNotFound()

def is_delete_reply_comment_post(request):
	return request.method == "POST" and request.POST.get("form_type") == "delete_reply_form"


def delete_reply_comment(request):
	try:
		reply = Comment.objects.get(pk=request.POST.get('reply_clicked'))
		parent_comment = Comment.objects.get(pk=request.POST.get('parent_comment'))
		parent_comment.replies.remove(reply)
	except:
		raise Http404(f"Could not delete reply comment")
		return HttpResponseNotFound()
	else:
		reply.delete()


