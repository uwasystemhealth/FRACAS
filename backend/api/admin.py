from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Comment, Record, Subsystem, Team
from .forms import UserChangeForm, UserCreationForm
User = get_user_model()


# A rewritten UserAdmin method to work with a customized AbstractBaseUser
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#auth-custom-user
# ------------------------------------------------------------------------------
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ["password"]}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "username", "team", "email")},
        ),
    )
    list_filter = [
        "is_admin",
        "team",
    ]
    list_display = [
        "first_name",
        "last_name",
        "team",
        "username",
        "email",
    ]
    search_fields = ["first_name", "last_name", "team", "username", "email"]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]

# unregister unused django default Group model from admin
# ------------------------------------------------------------------------------
admin.site.unregister(Group)

# team admin
# ------------------------------------------------------------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["team_name", "team_lead"]


# subsystem admin
# ------------------------------------------------------------------------------
@admin.register(Subsystem)
class SubsystemAdmin(admin.ModelAdmin):
    list_display = ["subsystem_name", "parent_team"]


# record admin
# ------------------------------------------------------------------------------
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [
        "record_creation_time",
        "status",
        "team",
        "subsystem",
        "record_creator",
        "car_year",
    ]
    list_filter = [
        "record_creation_time",
        "status",
        "team",
        "subsystem",
        "record_creator",
        "car_year",
    ]


# comment admin
# ------------------------------------------------------------------------------
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        "comment_text",
        "commenter",
        "creation_time",
        "record_id",
    ]
    ordering = ["creation_time"]
    list_filter = ["creation_time", "commenter", "record_id"]