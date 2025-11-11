from django import forms
from django.contrib.auth import authenticate

class LogInForm(forms.Form):
    """
    Form enabling registered users to log in.

    This simple login form collects a username and password and attempts
    to authenticate the user against Django’s authentication backend.
    It does not handle the actual login process (session creation), which
    is typically done in a view using `django.contrib.auth.login()`.

    Fields:
        username (CharField): The username of the user.
        password (CharField): The user's password, rendered as a password input.
    """

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """
        Attempt to authenticate the user with the provided credentials.

        This method should be called after form validation (`is_valid()`).
        It retrieves the cleaned username and password from the form data
        and uses Django’s built-in `authenticate()` function to verify them.
        """

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user