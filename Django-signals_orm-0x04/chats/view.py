from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message


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
