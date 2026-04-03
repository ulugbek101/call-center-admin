from django.db import models


class UserRoles(models.TextChoices):
    SUPERUSER = 'superuser', 'Супер-пользователь'
    STAFF = 'staff', 'Сотрудник'
