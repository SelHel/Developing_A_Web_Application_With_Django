from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Ticket, UserFollows
from .forms import ReviewForm, TicketForm


@login_required
def flux(request):
    tickets = Ticket.objects.all()
    return render(request, 'blog/flux.html', context={'tickets': tickets})


@login_required
def ticket_creation(request):
    """Permet la création d'un ticket."""
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')

    return render(request, 'blog/ticket_creation.html', context={'ticket_form': ticket_form})


@login_required
def ticket_modification(request, ticket_id):
    """Permet la modification d'un ticket."""
    pass


@login_required
def ticket_deletion(request, ticket_id):
    """Permet la suppression d'un ticket."""
    pass


@login_required
def review_creation(request):
    """Permet la création d'une critique sans réponse à un ticket."""
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket_recorded = Ticket.objects.last()
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket_recorded
            review.user = request.user
            review.save()
            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }

    return render(request, 'blog/review_creation.html', context=context)


@login_required
def ticket_review_creation(request, ticket_id):
    """"Permet la création d'une critique en réponse à un ticket."""
    pass

@login_required
def review_modification(request, review_id):
    """Permet la modification d'une critique."""
    pass


@login_required
def review_deletion(request, review_id):
    """Permet la suppression d'une critique."""
    pass


@login_required
def subscriptions(request):
    connected_user = request.user
    all_followers = UserFollows.objects.filter(followed_user=connected_user)
    all_followed = UserFollows.objects.filter(user=connected_user)

    if request.method == 'POST':
        to_follow = request.POST['username']
        try:
            user_to_follow = User.objects.get(username=to_follow)

            UserFollows.objects.create(
                user=request.user,
                followed_user=user_to_follow
            )
        except:
            print('user non existing!')

    return render(
        request, 'blog/subscriptions.html', context={'all_followers': all_followers, 'all_followed': all_followed})


@login_required
def unsubscribe(request, user_follows_id):
    connection = UserFollows.objects.filter(id=user_follows_id)
    connection.delete()
    return redirect('subscriptions')
