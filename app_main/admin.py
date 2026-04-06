from django.contrib import admin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from app_main.models import User, Milestone


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ModelAdmin):
    search_help_text = "Поиск по ФИО, Номер телефона"
    list_display = (
        'id',
        'first_name',
        'last_name',
        'middle_name',
        'role_display',
        'is_on_vacation',
        'is_staff',
        'created',
        'updated',
    )
    list_display_links = (
        'id',
        'first_name',
        'last_name',
        'middle_name',
        'role_display',
        'created',
        'updated',
    )
    list_filter = ('role', 'is_on_vacation', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone_number')
    list_editable = ('is_on_vacation', 'is_staff')
    list_per_page = 20

    @admin.display(description='Телефон', ordering='phone_number')
    def phone_number_display(self, obj):
        return str(obj.phone_number) if obj.phone_number else '-'

    @admin.display(description='Роль', ordering='role')
    def role_display(self, obj):
        return obj.get_role_display()

    fieldsets = (
        ("Основные поля", {
            "fields": (
                "first_name", "last_name", "middle_name", "phone_number"
            )
        }),
        # Поле "password" - отключено
        # ("Безопасность", {
        #     "fields": (
        #         "password",
        #     ),
        #     "description": "Пароль зашифрован в целях безопасности, что бы изменить пароль - просто удалите старое значение и наберите новое",
        # }),
        ("Другое", {
            "fields": (
                "role", "current_score", "current_milestone", "is_on_vacation", "is_staff", "is_superuser", "is_active"
            )
        }),
    )


@admin.register(Milestone)
class MilestoneAdmin(ModelAdmin):
    search_help_text = "Поиск по названию этапа"
    fieldsets = (
        (None, {
            "fields": (
                "name", "required_score", "is_active",
            )
        }),
    )

    list_display = (
        "id",
        "name",
        "required_score",
        "is_active",
        "created",
        "updated",
    )
    list_display_links = (
        "id",
        "name",
        "is_active",
        "created",
        "updated",
    )
    list_filter = ('created',)
    search_fields = ('name',)
    list_editable = ('required_score',)
    list_per_page = 20
