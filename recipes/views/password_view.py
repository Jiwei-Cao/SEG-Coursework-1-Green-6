from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse
from recipes.forms import PasswordForm


class PasswordView(LoginRequiredMixin, FormView):
    """
    Allow authenticated users to change their password.

    This view presents a password change form and handles form submission.
    It ensures that only logged-in users can access the page. Upon a successful
    password update, the user is re-authenticated to maintain their session.
    """

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """
        Provide additional keyword arguments to the form.

        Specifically, the current authenticated user is passed to the form,
        which allows the `PasswordForm` to validate the old password and
        update the correct user instance.
        """

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        Handle successful password form submission.

        If the form validates successfully, the user's password is updated.
        The user is then re-authenticated to maintain their session without
        requiring them to log in again.
        """

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Determine the URL to redirect to after a successful password change.

        Also adds a success message to notify the user that their password
        was updated successfully.
        """

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')