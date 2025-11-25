from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message, User

@login_required
def send_message(request, receiver_id):
    """
    Send a message from the logged-in user to another user.
    """
    receiver = get_object_or_404(User, pk=receiver_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(
                sender=request.user,   # sender is the logged-in user
                receiver=receiver,
                content=content
            )
        return redirect("conversation", receiver_id=receiver.id)

    return render(request, "send_message.html", {"receiver": receiver})


@login_required
def conversation_view(request, receiver_id):
    """
    Fetch all messages between the logged-in user and another user.
    Use select_related to optimize foreign key queries.
    """
    receiver = get_object_or_404(User, pk=receiver_id)

    messages = (
        Message.objects
        .filter(
            sender=request.user, receiver=receiver
        ) | Message.objects.filter(
            sender=receiver, receiver=request.user
        )
    ).select_related('sender', 'receiver', 'parent_message', 'edited_by').order_by('timestamp')

    return render(request, "conversation.html", {
        "messages": messages,
        "receiver": receiver
    })

@login_required
def inbox_view(request):
    """
    Display only unread messages for the logged-in user, optimized with .only().
    """
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, "inbox.html", {
        "unread_messages": unread_messages
    })

@cache_page(60)  # ← cache for 60 seconds
@login_required
def conversation_messages(request, user_id):
    messages = (
        Message.objects
        .filter(sender_id=request.user.id, receiver_id=user_id)
        .select_related('sender', 'receiver')
        .order_by('timestamp')
    )

    return render(request, "conversation.html", {"messages": messages})