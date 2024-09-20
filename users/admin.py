from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User , Agent , Homeowner , Assistant , Contact
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Personal info', {'fields': ('name','phone', 'company', 'state', 'business_address', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'name','phone', 'company', 'state', 'business_address','is_verified'),
        }),
    )
    
    list_display = ('email',  'role', 'is_verified', 'is_staff')
    search_fields = ('email', 'phone', 'company')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)
admin.site.register(Agent)
admin.site.register(Homeowner)
admin.site.register(Assistant)
admin.site.register(Contact)