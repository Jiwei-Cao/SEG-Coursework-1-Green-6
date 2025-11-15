from django.contrib.auth.decorators import login_required 
from recipes.models import User 
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

@login_required
def user_list(request):
    query = request.GET.get('q', '').strip()

    users = User.objects.exclude(id=request.user.id)
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) 
        )

    following_ids = set(request.user.following.values_list('id', flat=True))

    context = {
        'users': users,
        'following_ids': following_ids,
        'query': query,
    }

    return render(request, 'user_list.html', context)

@login_required 
def follow_user(request, user_id):
    if request.method == 'POST':
        target = get_object_or_404(User, id=user_id)

        if target != request.user:
            request.user.following.add(target) 
        
    return redirect(request.META.get('HTTP_REFERER', reverse('user_list')))

@login_required 
def unfollow_user(request, user_id):
    if request.method == 'POST':
        target = get_object_or_404(User, id=user_id) 
        
        if target != request.user:
            request.user.following.remove(target)

    return redirect(request.META.get('HTTP_REFERER'), reverse('user_list'))