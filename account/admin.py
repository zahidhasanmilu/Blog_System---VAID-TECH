from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile

# Get the active User model (CustomUser)
User = get_user_model()

# -----------------------------
# Register User model in admin
# -----------------------------
admin.site.register(User)


# -----------------------------
# Register Profile model in admin
# -----------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    Shows user info, age, date of birth, and address.
    """

    # Columns to display in the admin list view
    list_display = ("user", "get_age", "date_of_birth", "address")

    # Fields that can be searched in admin
    search_fields = ("user__email", "user__username")

    # Filters available in the right sidebar
    list_filter = ("date_of_birth",)

    # --------------------------------
    # Method to show the age property
    # --------------------------------
    def get_age(self, obj):
        """
        Returns age from Profile's age property.
        Used in list_display to show computed age in admin.
        """
        return obj.age

    # Column header in admin list view
    get_age.short_description = "Age"
