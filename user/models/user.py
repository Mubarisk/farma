from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class Manager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields["is_superuser"] = True
        super(Manager, self).create_superuser(
            username, email, password, **extra_fields
        )


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STAFF = "STAFF", _("Staff")
        INVENTORY_MANAGER = "INVENTORY_MANAGER", _("Inventory Manager")

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.STAFF
    )

    def __str__(self):
        return self.username

    objects = Manager()
