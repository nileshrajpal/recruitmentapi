from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User


class Application(models.Model):
    objects = models.Manager()

    posted_by = models.OneToOneField(User, related_name='application',
                                     on_delete=models.CASCADE)
    posted_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"application of username {self.posted_by.username}"


class Education(models.Model):
    objects = models.Manager()

    qualification = models.CharField(max_length=255)
    passing_year = models.IntegerField()
    college = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    percentage = models.FloatField()
    application = models.ForeignKey(Application, related_name='education', on_delete=models.CASCADE)
