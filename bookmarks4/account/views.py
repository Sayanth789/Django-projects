from django.contrib import messages
from actions.models import Action
from actions.utils import create_action
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from . forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
    )
from .models import Profile , Contact


User = get_user_model()


@require_POST 
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                )
            return JsonResponse({'status':'ok'})
        except user.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status': 'error'})        



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {'section':'people', 'users':users}
    )

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        'account/user/detail.html',
        {'section':'people', 'user': user}
    )
# these are (above): simple list and detail view of User objects.


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

    

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            # Create a new user object but avoid saving it yet.
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user object.

            new_user.save()
            # Create the user profile.
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account ')
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else: 
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form':user_form}
    )    



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else: 
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})         

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user id following others, retrieves only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related(
            'user', 'user__profile'
        ).prefetch_related('target')[:10]
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard', 'actions': actions}
    )

# Here you retrieve all actions from the DB, excluding the ones performed by the current user.

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/profile_detail.html', {'user':user})
