from django.contrib.auth.decorators import login_required 
from recipes.models import User 
from django.db.models import Q, Count
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

@login_required
def user_search(request):
    query = request.GET.get('q', '').strip()

    users = User.objects.exclude(id=request.user.id)

    if query:
        filtered = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )           
        top_users = (
            filtered
            .annotate(follower_count=Count("followers"))
            .order_by("-follower_count")[:10]
        )
        has_query = True
    else:
        top_users = User.objects.none()
        has_query = False

    following_ids = set(request.user.following.values_list('id', flat=True))

    context = {
        "query": query,
        "users": users,
        "top_users": top_users,
        "following_ids": following_ids,
        "has_query": has_query,
    }

    return render(request, 'user_search.html', context)

@login_required 
def follow_user(request, user_id):
    if request.method != 'POST':
        return redirect("user_search")

    target = get_object_or_404(User, id=user_id)

    if target != request.user:
        request.user.following.add(target) 
        
    return redirect('user_search')

@login_required 
def unfollow_user(request, user_id):
    if request.method != 'POST':
        return redirect("user_search")

    target = get_object_or_404(User, id=user_id) 
    
    if target != request.user:
        request.user.following.remove(target)

    return redirect('user_search')
