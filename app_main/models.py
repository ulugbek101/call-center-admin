from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from phonenumber_field.modelfields import PhoneNumberField

from app_main.enums import UserRoles
from app_main.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", unique=True)
    role = models.CharField(verbose_name="Роль", max_length=50, choices=UserRoles.choices, default=UserRoles.STAFF)
    current_score = models.IntegerField(verbose_name="Текущий балл", default=0)
    current_milestone = models.ForeignKey('Milestone', verbose_name="Текущий этап", on_delete=models.PROTECT, blank=True, null=True)

    is_on_vacation = models.BooleanField(verbose_name="На отпуске", help_text="Включите, если сотрудник на отпуске или по какой то причине долго не может работать", default=False)
    is_active = models.BooleanField(verbose_name="Активный", help_text="Статус активности пользователя, вместо того что бы удалить пользователя, просто отключите эту опцию", default=True)
    is_superuser = models.BooleanField(verbose_name="Суперпользователь", help_text="Может ли сотрудник создавать и удалять других сотрудников", default=False)
    is_staff = models.BooleanField(verbose_name="Сотрудник", help_text="Может ли сотрудник заходить в админ панель", default=False)

    created = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "middle_name"]

    def get_username(self):
        return self.phone_number.__str__()

    def get_fullname(self):
        return self.__str__()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    class Meta:
        db_table = "users"
        ordering = ['-created']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ("first_name", "last_name", "middle_name")

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Milestone(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    required_score = models.IntegerField(verbose_name="Необходимый балл", help_text="Минимальный балл для достижения этого этапа")
    is_active = models.BooleanField(verbose_name="Активно", help_text="Вместо того, что бы удалить - просто деактивируйте этап", default=True)
    created = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "milestones"
        ordering = ["required_score", "is_active", "-created"]
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"



class FinishedMilestones(models.Model):
    milestone = models.ForeignKey(verbose_name="Этап", to=Milestone, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name="Сотрудник", to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.user.get_fullname()} - {self.milestone.name}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "Завершенный этап"
        verbose_name_plural = "Завершенные этапы"
