from django.contrib import admin
from .models import Service, VideoEmbed, SocialAndAppSettings

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_featured')

@admin.register(VideoEmbed)
class VideoEmbedAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'is_active')

@admin.register(SocialAndAppSettings)
class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)