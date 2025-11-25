from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
