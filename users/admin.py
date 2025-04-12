from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # this is for admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'phone_number')}),
        ('permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields':('last_login', 'date_joined')})
    )

    # this is for new user
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ('email', )
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
