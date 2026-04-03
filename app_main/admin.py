from django.contrib import admin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from app_main.models import User, Milestone


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ModelAdmin):
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


@admin.register(Milestone)
class MilestoneAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'required_score',
        'created',
        'updated',
    )
    list_display_links = (
        'id',
        'name',
        'created',
        'updated',
    )
    list_filter = ('created', 'updated')
    search_fields = ('name',)
    list_editable = ('required_score',)
    list_per_page = 20
