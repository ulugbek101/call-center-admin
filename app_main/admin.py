from unfold import admin
from app_main.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'phone_number', 'get_role_display', 'is_on_vacation', 'is_active', 'is_superuser', 'is_staff', 'created', 'updated')
    list_filter = ('role', 'is_on_vacation', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone_number')
    ordering = ('-created',)
    list_editable = ('is_on_vacation', 'is_active', 'is_superuser', 'is_staff')
    list_per_page = 20
