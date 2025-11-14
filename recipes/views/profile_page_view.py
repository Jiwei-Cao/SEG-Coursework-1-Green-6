from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from math import floor

recipes = [
    {
        'title': 'Chicken Stroganoff',
        'description': 'Use chicken thigh fillets if you prefer in this chicken stroganoff, and use half-fat soured cream for a lighter version. Enjoy with pasta, mash or rice.',
        'img':'https://images.immediate.co.uk/production/volatile/sites/30/2022/09/Chicken-Stroganoff-06462c0.jpg?quality=90&webp=true&resize=556,505'
    },
    {
        'title': 'Chicken and Bacon Pie',
        'description': 'Top our creamy chicken pie with puff pastry for a satisfying family-friendly meal. Easy to freeze (unbaked), enjoy with your favourite veg',
        'img':'https://images.immediate.co.uk/production/volatile/sites/30/2023/12/Chicken-and-bacon-pie-f26cc35.jpg?quality=90&resize=556,505'
    },
    {
        'title': 'Chicken Chow Mein',
        'description': 'This Taiwanese-style chow mein uses a combination of stir-frying and steaming, so theres less oil involved. Pork would also work well instead of chicken',
        'img':'https://images.immediate.co.uk/production/volatile/sites/30/2022/06/Chicken-chow-mein-7aeec1d.png?quality=90&resize=556,505'
    },
    {
        'title': 'Chicken Chow Mein',
        'description': 'This Taiwanese-style chow mein uses a combination of stir-frying and steaming, so theres less oil involved. Pork would also work well instead of chicken',
        'img':'https://images.immediate.co.uk/production/volatile/sites/30/2022/06/Chicken-chow-mein-7aeec1d.png?quality=90&resize=556,505'
    },
    {
        'title': 'Chicken Chow Mein',
        'description': 'This Taiwanese-style chow mein uses a combination of stir-frying and steaming, so theres less oil involved. Pork would also work well instead of chicken',
        'img':'https://images.immediate.co.uk/production/volatile/sites/30/2022/06/Chicken-chow-mein-7aeec1d.png?quality=90&resize=556,505'
    },
]

@login_required
def profile_page(request):
    """
    Display's the current user's profile.
    """
    
    current_user = request.user
    rating = round(current_user.rating * 2) / 2
    full_stars = int(floor(rating))
    half_star = rating-full_stars==0.5
    empty_stars = 5 - full_stars - half_star

    return render(request, 'profile_page.html', {
        'user': current_user,
        'recipes':recipes,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars)
        })