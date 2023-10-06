from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Team

UserModel = get_user_model()


def register_validation(data):
    """Validates the data for user registration.

    Args:
        data (dict): A dictionary containing the user data.

    Returns:
        dict: The validated data with the password and team fields set.

    Raises:
        ValidationError: If the email is already taken, the password is too short, or the passwords do not match.
    """
    email = data["email"].strip()
    first_name = data["first_name"].strip()
    last_name = data["last_name"].strip()
    password1 = data["password1"].strip()
    password2 = data["password2"].strip()
    team = data["team"].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise serializers.ValidationError("Email taken: choose another email.")
    if not password1 or len(password1) < 8:
        raise serializers.ValidationError("Choose another password, min 8 characters.")
    if not first_name:
        raise serializers.ValidationError("First name is required.")
    if not last_name:
        raise serializers.ValidationError("Last name is required.")
    if not password2 or password1 != password2:
        raise serializers.ValidationError("Passwords must match.")
    else:
        data["password"] = password1
        data.pop("password1")
        data.pop("password2")
    if not team or not Team.objects.filter(team_name__iexact=team).exists():
        # team not found or not provided: silently assigns null
        # can change this later
        data["team"] = None
    else:  # team found case insensitive exact match (__iexact)
        data["team"] = Team.objects.get(team_name__iexact=team).pk
        # new registered user is not staff or admin
        data["is_staff"] = False
        data["is_admin"] = False
    return data
