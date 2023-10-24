from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Log


# admin.site.register(CustomUser, UserAdmin)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "otp")}),
        ("Personal info", {"fields": ("first_name", "last_name", "mobile")}),
        ("Permissions",
         {
             "fields": (
                 "is_active",
                 "is_staff",
                 "is_superuser",
                 "groups",
                 "user_permissions",
             ),
         },
         ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


class LogModelAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'created_on')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Log, LogModelAdmin)
