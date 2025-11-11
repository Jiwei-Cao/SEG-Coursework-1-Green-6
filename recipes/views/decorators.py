from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect


def login_prohibited(view_function):
    """
    Decorator that prevents logged-in users from accessing a view.

    This decorator is typically used for pages such as login or registration,
    where it doesn't make sense for an authenticated user to remain.
    If the user is already authenticated, they are redirected to the URL
    defined in `settings.REDIRECT_URL_WHEN_LOGGED_IN`.

    Args:
        view_function (Callable): The Django view function being decorated.

    Returns:
        Callable: A wrapped view function that either redirects an authenticated
        user or calls the original view for unauthenticated users.

    Raises:
        ImproperlyConfigured: If `settings.REDIRECT_URL_WHEN_LOGGED_IN` is not defined.
    """
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function


class LoginProhibitedMixin:
    """
    Mixin that prevents logged-in users from accessing certain class-based views.

    This mixin is useful for class-based views such as LoginView or SignupView,
    where authenticated users should not be able to access the page. It redirects
    them to a specified URL instead.

    Attributes:
        redirect_when_logged_in_url (str): Optional. The URL to redirect to if
            the user is already logged in. Must be defined either as a class
            attribute or by overriding `get_redirect_when_logged_in_url()`.
    """

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """
        Intercept requests before they reach the view handler.

        If the user is authenticated, redirects them using
        `handle_already_logged_in()`. Otherwise, proceeds normally.
        """
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        """
        Redirect the user when already logged in.
        """
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """
        Determine the redirect URL for authenticated users.

        If the `redirect_when_logged_in_url` attribute is not defined,
        this method must be overridden in a subclass. Otherwise, an
        `ImproperlyConfigured` exception is raised.
        """
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url