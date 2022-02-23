from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import CharField, Value

from itertools import chain

from .models import Ticket, Review, UserFollows
from .forms import ReviewForm, TicketForm


def get_users_viewable_tickets(user):
    all_tickets = []
    all_followed = UserFollows.objects.filter(user=user)
    followed_users = [elm.followed_user for elm in all_followed]
    if user not in followed_users:
        followed_users.append(user)

    all_tickets = Ticket.objects.filter(user__in=followed_users)
    return all_tickets


def get_users_viewable_reviews(user):
    all_followed = UserFollows.objects.filter(user=user)
    followed_users = [elm.followed_user for elm in all_followed]
    if user not in followed_users:
        followed_users.append(user)

    all_followed_reviews = Review.objects.filter(user__in=followed_users)
    all_followed_tickets = get_users_viewable_tickets(user)
    all_reviews_to_tickets_of_followed = Review.objects.filter(ticket__in=all_followed_tickets)
    return all_followed_reviews, all_reviews_to_tickets_of_followed


@login_required
def flux(request):
    reviews = get_users_viewable_reviews(request.user)
    reviews_0 = reviews[0].annotate(content_type=Value('REVIEW', CharField()))
    reviews_1 = reviews[1].annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        set(chain(reviews_0, reviews_1, tickets)),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/flux.html', context={'posts': posts})


@login_required
def posts(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/posts.html', context={'posts': posts})


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
            messages.success(request, "Votre ticket a bien été créé.")
            return redirect('flux')

    return render(request, 'blog/ticket_creation.html', context={'ticket_form': ticket_form})


@login_required
def ticket_modification(request, ticket_id):
    """Permet la modification d'un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        messages.warning(request, "Vous n'êtes pas autorisé à modifier ce ticket.")
        return redirect('logout')
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre ticket a bien été modifié.")
            return redirect('posts')
    else:
        ticket_form = TicketForm(instance=ticket)

    return render(request, 'blog/ticket_modification.html', context={'ticket_form': ticket_form})


@login_required
def ticket_deletion(request, ticket_id):
    """Permet la suppression d'un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        messages.warning(request, "Vous n'êtes pas autorisé à supprimer ce ticket.")
        return redirect('logout')
    ticket.delete()
    messages.success(request, "Votre ticket a bien été supprimé.")
    return redirect('posts')


@login_required
def ticket_confirm_deletion(request, ticket_id):
    """Permet de confirmer la suppression d'un ticket."""
    previous_page = request.META.get('HTTP_REFERER', '/')
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, 'blog/ticket_confirm_deletion.html',
                  context={'post': ticket, 'previous_page': previous_page})


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
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.rating = request.POST.get('rating')
            review.user = request.user
            review.save()
            messages.success(request, "Votre critique a bien été créée.")
            return redirect('flux')

    return render(request, 'blog/review_creation.html',
                  context={'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def ticket_review_creation(request, ticket_id):
    """"Permet la création d'une critique en réponse à un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a bien été créée.")
            return redirect('flux')
    else:
        review_form = ReviewForm(instance=ticket)

    return render(request, 'blog/ticket_review_creation.html',
                  context={'review_form': review_form, 'post': ticket})


@login_required
def review_modification(request, review_id):
    """Permet la modification d'une critique."""
    review = get_object_or_404(Review, id=review_id)
    ticket = Ticket.objects.get(id=review.ticket.id)
    if review.user != request.user:
        messages.warning(request, "Vous n'êtes pas autorisé à modifier cette critique.")
        return redirect('logout')
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a bien été modifiée.")
            return redirect('posts')
    else:
        review_form = ReviewForm(instance=review)

    return render(request, 'blog/review_modification.html', context={'review_form': review_form, 'post': ticket})


@login_required
def review_deletion(request, review_id):
    """Permet la suppression d'une critique."""
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        messages.warning(request, "Vous n'êtes pas autorisé à supprimer cette critique.")
        return redirect('logout')
    review.delete()
    messages.success(request, "Votre critique a bien été supprimée.")
    return redirect('posts')


@login_required
def review_confirm_deletion(request, review_id):
    """Permet de confirmer la suppression d'une critique."""
    previous_page = request.META.get('HTTP_REFERER', '/')
    review = get_object_or_404(Review, id=review_id)

    return render(request, 'blog/review_confirm_deletion.html',
                  context={'post': review, 'previous_page': previous_page})


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
