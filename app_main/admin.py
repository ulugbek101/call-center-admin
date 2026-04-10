from django.contrib import admin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from app_main.models import User, Milestone, MotivationalPhrase, Point


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ModelAdmin):
    search_help_text = "Поиск по ФИО, Номер телефона"
    list_display = (
        'id',
        'first_name',
        'last_name',
        'is_activation_code_used',
        'activation_code',
        'created',
        'updated',
    )
    list_display_links = (
        'id',
        'first_name',
        'last_name',
        'telegram_id',
        'is_activation_code_used',
        'created',
        'updated',
    )
    list_filter = ('role', 'is_on_vacation', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'telegram_id')
    list_per_page = 20

    @admin.display(description='Телефон', ordering='phone_number')
    def phone_number_display(self, obj: User):
        return str(obj.phone_number) if obj.phone_number else '-'

    @admin.display(description='Роль', ordering='role')
    def role_display(self, obj: User):
        return obj.get_role_display()

    fieldsets = (
        ("Основные поля (Обязательно)", {
            "fields": (
                "first_name", "last_name", "middle_name", "phone_number"
            )
        }),
        ("Другое (Не обязательно)", {
            "fields": (
                "telegram_id", "role", "activation_code", "is_activation_code_used", "is_on_vacation", "is_staff", "is_superuser", "is_active"
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


@admin.register(MotivationalPhrase)
class MotivationalPhrasesAdmin(ModelAdmin):
    search_help_text = "Поиск по фрагменту фразы"
    list_display = ["id", "phrase", "created"]
    list_filter = ["created"]
    search_fields = ["name"]
    list_per_page = 20


@admin.register(Point)
class PointAdmin(ModelAdmin):
    autocomplete_fields = ["user"]
    search_help_text = "Поиск по фрагменту причины вознаграждения"
    list_display = ["id", "first_name_display", "last_name_display", "amount", "created"]
    list_filter = ["created"]
    search_fields = ["user__first_name", "user__last_name", "description"]
    list_per_page = 20

    @admin.display(description="Имя", ordering="user__first_name")
    def first_name_display(self, obj: Point):
        return obj.user.first_name

    @admin.display(description="Фамилия", ordering="user__last_name")
    def last_name_display(self, obj: Point):
        return obj.user.last_name

