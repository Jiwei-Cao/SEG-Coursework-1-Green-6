from django.conf import settings
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse
from recipes.forms import SignUpForm
from recipes.views.decorators import LoginProhibitedMixin


class SignUpView(LoginProhibitedMixin, FormView):
    """
    Handle new user registration.

    This class-based view displays a registration form for new users and handles
    the creation of their accounts. Authenticated users are automatically
    redirected away using `LoginProhibitedMixin`.
    """

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        """
        Handle valid signup form submissions.

        When the signup form is submitted and validated successfully, a new
        user account is created, and the user is automatically logged in.
        Afterward, the method continues to the success URL defined by
        `get_success_url()`.
        """
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Determine the redirect URL after successful registration.
        """
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)