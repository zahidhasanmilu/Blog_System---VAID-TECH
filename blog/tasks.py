# blog/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model  # To get the CustomUser model

# Load your CustomUser model
User = get_user_model()


@shared_task
def send_new_post_notification_email(post_title, post_url):
    """
    Sends email notifications to all active registered users when a new blog post is published.
    This task runs asynchronously in the background via Celery.
    """

    # 1. Retrieve the email list of all active and non-staff users
    recipient_list = list(
        User.objects.filter(
            is_active=True, is_staff=False
        ).values_list(  # Filter for active and regular users only
            "email", flat=True
        )
    )

    if not recipient_list:
        print("Celery: No active users found to send email.")
        return "No active users found."

    subject = f"New Blog Post Alert: {post_title}"
    message = f"""
Dear Reader,

We have just published a new blog post! 
Title: {post_title}

Click here to read:
{post_url}

Thank you for being a part of our community.
"""
    # Get the sender email address from settings.py
    email_from = settings.DEFAULT_FROM_EMAIL or "no-reply@yourblog.com"

    print(f"Celery: Sending notification to {len(recipient_list)} active users.")

    # 2. Call the main Django function to send the email
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False,  # Set to True to suppress exceptions
    )

    return f"Notification email sent successfully to {len(recipient_list)} users for post: {post_title}"
