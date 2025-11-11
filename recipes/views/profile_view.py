from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from recipes.forms import UserForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allow authenticated users to view and update their profile information.

    This class-based view displays a user profile editing form and handles
    updates to the authenticated user’s profile. Access is restricted to
    logged-in users via `LoginRequiredMixin`.
    """

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """
        Retrieve the user object to be edited.

        This ensures that users can only update their own profile, rather
        than any other user’s data.

        Returns:
            User: The currently authenticated user instance.
        """
        user = self.request.user
        return user

    def get_success_url(self):
        """
        Determine the redirect URL after a successful profile update.

        Also adds a success message to inform the user that their profile
        was successfully updated.

        Returns:
            str: The URL to redirect to (typically the dashboard or user home).
        """
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)