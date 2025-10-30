from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Render per-user dashboard. JS will call API endpoints using user_id.
    """
    user = request.user
    context = {
        "user_id": str(user.id),
        "user_full_name": user.get_full_name() or getattr(user, "phone_number", user.username)
    }
    return render(request, "dashboard.html", context)
