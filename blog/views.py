from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'tickets': tickets})


@login_required
def ticket_creation(request):
    pass


@login_required
def subscriptions(request):
    connected_user = request.user
    all_followers = models.UserFollows.objects.filter(followed_user=connected_user)
    all_followed = models.UserFollows.objects.filter(user=connected_user)

    if request.method == 'POST':
        to_follow = request.POST['username']
        try:
            user_to_follow = User.objects.get(username=to_follow)

            models.UserFollows.objects.create(
                user=request.user,
                followed_user=user_to_follow
            )
        except:
            print('user non existing!')

    return render(
        request, 'blog/subscriptions.html', context={'all_followers': all_followers, 'all_followed': all_followed})


@login_required
def unsubscribe(request, user_follows_id):
    connection = models.UserFollows.objects.filter(id=user_follows_id)
    connection.delete()
    return redirect('subscriptions')
