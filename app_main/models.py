from random import randint

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from phonenumber_field.modelfields import PhoneNumberField

from app_main.enums import UserRoles
from app_main.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="Имя", max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255, blank=True, null=True)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", unique=True)
    telegram_id = models.CharField(verbose_name="Телеграмм ID", max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name="Роль", max_length=50, choices=UserRoles.choices, default=UserRoles.STAFF)

    activation_code = models.CharField(verbose_name="Код активации", max_length=10, help_text="НЕ ЗАПОЛНЯЙТЕ ЭТО ПОЛЕ. Код активации сгенерирутся АВТОМАТИЧЕСКИ", blank=True, null=True)
    is_activation_code_used = models.BooleanField(verbose_name="Использован ли код активации", default=False, help_text="Индикатор того, использовал ли сотрудник этот код при запуке бота")
    is_on_vacation = models.BooleanField(verbose_name="На отпуске", help_text="Включите, если сотрудник на отпуске или по какой то причине долго не может работать", default=False)
    is_active = models.BooleanField(verbose_name="Активный", help_text="Статус активности пользователя, вместо того что бы удалить пользователя, просто отключите эту опцию", default=True)
    is_superuser = models.BooleanField(verbose_name="Суперпользователь", help_text="Может ли сотрудник создавать и удалять других сотрудников", default=False)
    is_staff = models.BooleanField(verbose_name="Доверенный сотрудник", help_text="Может ли сотрудник заходить в админ панель", default=False)

    created = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    @property
    def current_score(self):
        points = self.point_set.values_list('amount')
        sum = 0
        for point in points:
            sum += point[0]
        return sum

    @property
    def current_milestone(self):
        user_milestone = ""

        milestones = Milestone.objects.all()

        for milestone in milestones:
            if self.current_score >= milestone.required_score:
                user_milestone = milestone.name

        return user_milestone

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

        if not self.activation_code:
            super().save(*args, **kwargs)
            self.activation_code = f"{self.id}{self.last_name[0].capitalize()}{randint(10, 50)}{self.first_name[0]}"

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
    milestone = models.ForeignKey(verbose_name="Этап", to=Milestone, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="Сотрудник", to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.user.get_fullname()} - {self.milestone.name}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "Завершенный этап"
        verbose_name_plural = "Завершенные этапы"
        db_table = "finished_milestones"



class MotivationalPhrase(models.Model):
    phrase = models.TextField(verbose_name="мотивирующая фраза", help_text="Длина не ограничена")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phrase[:50]} ..."

    class Meta:
        db_table = "motivational_phrases"
        verbose_name = "Мотивирующая фраза"
        verbose_name_plural = "Мотивирующие фразы"
        ordering = ["-created"]



class Point(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Сотрудник", help_text="Укажите сотрудника, кому выдается балл")
    amount = models.IntegerField(verbose_name="Кол-во баллов")
    description = models.CharField(verbose_name="За что сотрудник получает этот балл", max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_fullname()} получил {self.amount} балл за \"{self.description[:20]}\""

    class Meta:
        db_table = "points"
        verbose_name = "Балл"
        verbose_name_plural = "Быллы"
        ordering = ["-created", "amount"]
