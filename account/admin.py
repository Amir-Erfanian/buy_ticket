from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_editable = (
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = (
        "-date_joined",
    )

    fieldsets = (
        (
            "اطلاعات حساب",
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "اطلاعات شخصی",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "وضعیت حساب",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "دسترسی‌ها",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "تاریخ‌ها",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

