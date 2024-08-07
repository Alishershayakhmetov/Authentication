from django.contrib import admin
from .models import CustomUser, OtpToken
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email')}
         ),
    )


class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")


admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

