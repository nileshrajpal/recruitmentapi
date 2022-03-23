from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # If True, User is Admin else Candidate
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"username {self.username}"
