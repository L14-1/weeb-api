from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'get_role')
    list_filter = ('is_active', 'profile__role')
    actions = ['activate_users']

    @admin.display(description='Role')
    def get_role(self, obj):
        return obj.profile.role

    @admin.action(description='Activer les comptes sélectionnés')
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)