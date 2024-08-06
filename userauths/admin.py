from django.contrib import admin
from userauths.models import User, ContactUs, Profile  # Import Institution


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio', 'get_institution', 'is_approved']
    actions = ['approve_users']

    def get_institution(self, obj):
        try:
            return obj.profile.institution
        except Profile.DoesNotExist:
            return None
    
    get_institution.short_description = 'Institution'

    def approve_users(self, request, queryset):
        for user in queryset:
            user.is_approved = True
            user.save()
            user.send_approval_email()  # Send email notification
        self.message_user(request, "Selected users have been approved and notified via email.")
    
    approve_users.short_description = "Approve selected users"




class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']



# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'bio', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)
 # Register Institution
