from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_subscribed',
        'last_login'
    )
    search_fields = ('username', )
    list_filter = ('email', 'username', )


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe)
