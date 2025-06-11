<<<<<<< HEAD
from django.contrib import admin

# Register your models here.
=======
# authentication/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# یک کلاس inline برای نمایش Profile همراه با User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# سفارشی‌سازی UserAdmin اصلی
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'get_group', 'get_country', 'get_farm_address',
        'is_active', 'is_staff'
    )
    list_select_related = ('profile', )

    def get_group(self, instance):
        return instance.profile.group
    get_group.short_description = 'Group'
    get_group.admin_order_field = 'profile__group'

    def get_country(self, instance):
        return instance.profile.country
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'profile__country'

    def get_farm_address(self, instance):
        return instance.profile.farm_address
    get_farm_address.short_description = 'Farm Address'
    get_farm_address.admin_order_field = 'profile__farm_address'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


# ثبت تغییرات در پنل ادمین
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
>>>>>>> 7576c1d35bb7910344a6ac3a18c4a6d539cb55fd
