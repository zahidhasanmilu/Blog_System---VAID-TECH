from django.shortcuts import render, get_object_or_404
from .models import Profile

def User_ProfileView(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    user_blogs = profile_user.user.user_blogs.all()  # Assuming a related_name='blogs' in Blog model's ForeignKey to CustomUser
    
    context = {
        'profile_user': profile_user,
        'user_blogs': user_blogs,
    }
    return render(request, 'app_account/profile.html', context)
