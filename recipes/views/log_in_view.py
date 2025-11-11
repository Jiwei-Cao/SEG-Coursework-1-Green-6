from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from recipes.forms import LogInForm
from recipes.views.decorators import LoginProhibitedMixin


class LogInView(LoginProhibitedMixin, View):
    """
    Handle user login requests.

    This class-based view displays a login form for unauthenticated users
    and processes login submissions. Authenticated users are redirected
    away automatically via `LoginProhibitedMixin`.
    """

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """
        Handle GET requests by displaying the login form.
        """

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """
        Handle POST requests to authenticate and log in the user.

        This method attempts to authenticate the user based on submitted
        credentials. If successful, the user is logged in and redirected.
        Otherwise, an error message is displayed and the form is re-rendered.
        """

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """
        Render log in template with blank log in form.
        """

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})