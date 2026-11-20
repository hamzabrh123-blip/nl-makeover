from django.contrib import admin
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner, LegalPage, Certificate, VisitorLog
from .offer_models import SpecialOffer


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_tag', 'end_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(SocialAndAppSettings)
class SocialAndAppSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone_number', 'meta_title')

    fieldsets = (
        ('Basic Salon Details', {
            'fields': ('site_name', 'logo', 'phone_number', 'address')
        }),
        ('Homepage & Global SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'Yahan se Homepage ka Meta Title, Meta Description aur Meta Keywords change kar sakte hain.'
        }),
        ('Hero Section Content', {
            'fields': ('hero_tagline', 'hero_title', 'hero_description')
        }),
        ('Social Links & App APK', {
            'fields': ('whatsapp_channel_url', 'instagram_url', 'youtube_url', 'facebook_url', 'google_map_url', 'apk_file')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'slug', 'category', 'is_active', 'is_featured')
    list_editable = ('order', 'is_active', 'is_featured')
    list_display_links = ('title',)
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('title', 'slug', 'meta_title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'category', 'price', 'description', 'is_active', 'is_featured', 'order')
        }),
        ('Service Image & Alt Text (Required for SEO)', {
            'fields': ('image', 'image_alt')
        }),
        ('SEO & Google Ranking Settings', {
            'fields': ('slug', 'meta_title', 'meta_description'),
        }),
    )


@admin.register(VideoEmbed)
class VideoEmbedAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'is_active')
    list_filter = ('platform', 'is_active')


@admin.register(SliderBanner)
class SliderBannerAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'title', 'service', 'custom_url', 'is_active')
    list_editable = ('display_order', 'service', 'is_active')
    list_display_links = ('title',)
    list_filter = ('is_active', 'service')


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'display_order',
        'title',
        'certificate_number',
        'issuing_authority',
        'is_active',
    )
    list_editable = ('display_order', 'is_active')
    list_display_links = ('title',)
    list_filter = ('is_active',)
    search_fields = ('title', 'certificate_number', 'issuing_authority')
    ordering = ('display_order', '-created_at')
    readonly_fields = ('created_at',)


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('city', 'platform', 'page', 'ip_address', 'visited_at')
    list_filter = ('city', 'platform', 'page', 'visited_at')
    search_fields = ('city', 'ip_address')
    readonly_fields = ('city', 'platform', 'page', 'ip_address', 'visited_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False