from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Teacher


class MyUserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # This will show columns to display
    list_display = ('email','first_name', 'last_name', 'previous_login',
                    'last_login','is_staff','is_active','country','date_joined')
    search_fields=('email', 'first_name')
    readonly_fields=('date_joined','last_login','previous_login')
    filter_horizontal = ()
    list_filter= ('last_login',) #by school
    ordering = ('email',)
    model= Teacher
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets=(
        ('Personal info', {
            'classes': ('wide', 'extrapretty',), #there is collapse
            'fields': ('first_name','last_name',('country')) #display multiple fields in the same line
        }),
        ('Login info', {
            'description':("This is mandatory"),
            'classes': ('wide',),
            'fields': ('email',
                       'password1','password2', )
            }),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    fieldsets=()

# Now register the new UserAdmin...
admin.site.register(Teacher, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
