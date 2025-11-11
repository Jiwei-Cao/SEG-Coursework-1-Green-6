from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from recipes.models import User

class UserForm(forms.ModelForm):
    """
    Form to update user profile information.

    This form allows authenticated users to update their basic profile
    details such as first name, last name, username, and email address.
    It is typically used in a profile settings or account management page.
    """

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """
    Form mixin providing password and password confirmation fields.

    This mixin is intended to be used as a base for forms that require
    users to enter and confirm a new password (e.g., password reset,
    password change, or registration forms).

    It enforces basic password strength requirements and validates that
    the password and confirmation fields match.

    Fields:
        new_password (CharField): The new password entered by the user.
        password_confirmation (CharField): The repeated password used to
            confirm accuracy of the first input.
    """

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message=(
                    'Password must contain an uppercase character, '
                    'a lowercase character, and a number'
                )
            )
        ]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """
        Validate matching passwords and enforce password confirmation rules.

        This method ensures that the values entered in `new_password` and
        `password_confirmation` fields match. If they do not, an error is
        added to the `password_confirmation` field.

        Returns:
            dict: The cleaned form data.

        Raises:
            ValidationError: If the password and confirmation do not match.
        """
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error(
                'password_confirmation', 
                'Confirmation does not match password.'
            )


class PasswordForm(NewPasswordMixin):
    """
    Form enabling authenticated users to change their password.

    This form extends `NewPasswordMixin` to include validation for the user's
    **current password** before allowing a new password to be set. It is
    typically used in a “Change Password” or “Account Settings” page.
    """

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """
        Initialize the password form with the current user instance.

        Args:
            user (User, optional): The authenticated user who wants to change
                their password.
        """
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """
        Validate the current and new password fields.

        Ensures that:
        - The current password matches the user’s existing password.
        - The new password and confirmation fields (via `NewPasswordMixin`)
          match and meet complexity requirements.

        If any validation step fails, an appropriate error message is added
        to the form.

        Returns:
            dict: The cleaned form data.

        Raises:
            ValidationError: If the current password is incorrect or
            the new passwords do not match.
        """

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """
        Update the user's password with the new validated password.

        This method securely sets and saves the new password for the user
        instance associated with the form.

        Returns:
            User: The user instance with the updated password.
        """

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """
    Form enabling new users to register for an account.

    This form extends both `NewPasswordMixin` (for password and confirmation
    fields) and Django’s `ModelForm` to create a new `User` instance.
    It validates password strength and matching through the mixin, then
    creates the user with a hashed password using `create_user()`.

    Inherits from:
        NewPasswordMixin: Provides password validation and confirmation fields.
        forms.ModelForm: Generates form fields from the Django User model.

    Fields (in addition to those from NewPasswordMixin):
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        username (CharField): The desired username.
        email (EmailField): The user's email address.
    """

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """
        Create and return a new User instance.

        This method overrides the default `ModelForm.save()` to ensure
        that the password is hashed correctly and to integrate password
        validation provided by `NewPasswordMixin`.

        Returns:
            User: The newly created user instance.
        """

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user