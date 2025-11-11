from django.contrib.auth import logout
from django.shortcuts import redirect


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')