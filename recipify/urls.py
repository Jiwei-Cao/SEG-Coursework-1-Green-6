"""
URL configuration for recipify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin:index'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('profile_page/<str:username>/', views.profile_page, name='profile_page'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('cupboard/<int:ingredient_pk>/delete', views.delete_ingredient, name = 'delete_ingredient'),
    path('all_recipes/', views.browse_recipes, name='all_recipes'),
    path('recipe/<int:recipe_id>/', views.get_recipe, name="get_recipe"),
    path('user_search/', views.user_search, name="user_search"),
    path('user/<int:user_id>/follow/', views.follow_user, name="follow_user"),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name="unfollow_user"),
    path('cupboard/', views.cupboard, name="cupboard"),
    path('recipe/<int:recipe_id>/toggle_favourite', views.toggle_favourite, name='toggle_favourite'),
    path('select2/', include('django_select2.urls')),
    path('recipe/<int:recipe_id>/delete', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/edit', views.EditRecipeView.as_view(), name="edit_recipe"),
    path('users/<str:username>/', views.profile_page, name='user_profile'),
    path('users/<str:username>/following/', views.following_list, name="following_list"),
    path('users/<str:username>/followers/', views.followers_list, name="followers_list"),
    path('recipe/<int:recipe_id>/comment', views.handle_comments, name='handle_comments'),
    path('create_recipe/<int:recipe_id>/add_method/', views.add_method, name='add_method'),
    path('create_recipe/<int:recipe_id>/add_method/<int:step_id>/edit_method_step', views.edit_method_step, name='edit_method_step'),
    #path('manage_recipes', views.manage_recipes, name='manage_recipes'),
    path('manage_recipe_ingredient/<int:recipe_id>/', views.manage_recipe_ingredient, name='manage_recipe_ingredient'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
