from django.contrib import admin
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner, LegalPage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'category', 'price', 'is_featured')
    list_editable = ('order', 'is_featured')
    list_display_links = ('title',)  # Yeh zaroori hai jab pehla field ('order') editable ho
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')


@admin.register(VideoEmbed)
class VideoEmbedAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'is_active')
    list_filter = ('platform', 'is_active')


@admin.register(SliderBanner)
class SliderBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)


@admin.register(SocialAndAppSettings)
class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    readonly_fields = ('updated_at',)