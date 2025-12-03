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
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )           
        has_query = True
    else:

        has_query = False
    top_users = (
        users
        .exclude(id__in=request.user.following.values_list('id', flat=True))
        .annotate(follower_count=Count("followers"))
        .order_by("-follower_count")[:10])
    for user in top_users:
        user.follow_summary = get_follower_summary(user, request.user)

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
        
    return redirect('user_profile', username=target.username)

@login_required 
def unfollow_user(request, user_id):
    if request.method != 'POST':
        return redirect("user_search")

    target = get_object_or_404(User, id=user_id) 
    
    if target != request.user:
        request.user.following.remove(target)

    return redirect('user_profile', username=target.username)

def get_follower_summary(user, current_user):
    all_followers = list(user.followers.all())

    if not all_followers:
        return ""

    displayed_followers = []

    mutual_followers = [f for f in all_followers if f in current_user.following.all()]
    for f in mutual_followers[:2 - len(displayed_followers)]:
        displayed_followers.append(f.username)
        all_followers.remove(f)

    for f in all_followers[:3 - len(displayed_followers)]:
        displayed_followers.append(f.username)

    # 4. Calculate remaining count
    remaining_count = len(user.followers.all()) - len(displayed_followers)

    if remaining_count > 0:
        return f"Followed by {', '.join(displayed_followers)} + {remaining_count} others"
    else:
        return f"Followed by {', '.join(displayed_followers)}"
