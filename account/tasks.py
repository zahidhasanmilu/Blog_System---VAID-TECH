from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


@shared_task
def send_verification_email_task(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


#  SEND ENGAGEMENT EMAIL TO ALL ACTIVE USERS (PERIODIC)
@shared_task
def send_engagement_email_to_all_users():
    """
    Sends an engagement email to all active (non-staff) users.
    This will be triggered automatically by Celery Beat every 2 minutes.
    """

    # 1. Fetch all active, non-staff users
    active_users = User.objects.filter(is_active=True, is_staff=False).values_list(
        "email", flat=True
    )
    email_list = list(active_users)

    if not email_list:
        print("No active users found.")
        return "No active users found."

    subject = "Hello Bro, What's up?"
    message = (
        "Just checking in to see how you're doing and what new things you've built "
        "on the platform! Don't forget to check out our latest posts."
    )

    # 2. Send the email
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email
            email_list,  # To email list (will act as BCC)
            fail_silently=False,
        )
        print(f"✅ CELERY BEAT: Sent engagement email to {len(email_list)} users.")
        return f"Successfully sent email to {len(email_list)} users."

    except Exception as e:
        print(f"❌ CELERY BEAT ERROR: {e}")
        return f"Email sending failed: {e}"


# --------------------------
@shared_task
def print_current_time():
    """
    Example task: prints current time to console
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current Time: {now}")
    return now
