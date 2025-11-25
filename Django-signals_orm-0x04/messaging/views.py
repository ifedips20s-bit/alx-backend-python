from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their own account.
    """
    user = request.user
    if request.method == "POST":
        user.delete()  # Triggers post_delete signal
        messages.success(request, "Your account and all associated data have been deleted.")
        return redirect("home")  # Change 'home' to your actual homepage URL name
    return redirect("profile")  # Or wherever your delete confirmation page is

