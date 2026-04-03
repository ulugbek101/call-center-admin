from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, middle_name=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Пользователь должен иметь номер телефона')
        if not first_name:
            raise ValueError('Пользователь должен иметь имя')
        if not last_name:
            raise ValueError('Пользователь должен иметь фамилию')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, middle_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        return self.create_user(phone_number, first_name, last_name, middle_name, password, **extra_fields)
