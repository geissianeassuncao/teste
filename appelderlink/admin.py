from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "tipo", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Tipo de Usuário", {"fields": ("tipo",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Tipo de Usuário", {"fields": ("tipo",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
