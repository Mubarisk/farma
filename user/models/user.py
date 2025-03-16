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
    ADMIN = "admin"
    STAFF = "staff"
    STORE_MANAGER = "store_manager"
    ROLES = (
        (ADMIN, _("Admin")),
        (STAFF, _("Staff")),
        (STORE_MANAGER, _("Store Manager")),
    )

    role = models.CharField(max_length=20, choices=ROLES, default=STAFF)

    def __str__(self):
        return self.username

    objects = Manager()
