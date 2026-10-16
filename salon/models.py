from django.db import models


class SliderBanner(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Banner"

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Service Name")
    category = models.CharField(max_length=100, verbose_name="Category (e.g., Bridal, Hair)")
    price = models.CharField(max_length=50, verbose_name="Price / Starting From")
    description = models.TextField(verbose_name="Service Description")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Service Image")
    is_featured = models.BooleanField(default=False, verbose_name="Show on Home Page")

    def __str__(self):
        return self.title

class VideoEmbed(models.Model):
    PLATFORM_CHOICES = (
        ('youtube', 'YouTube Video / Short'),
        ('instagram', 'Instagram Reel / Post'),
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='youtube', verbose_name="Platform")
    title = models.CharField(max_length=150, verbose_name="Video Title / Caption")
    url = models.URLField(verbose_name="Instagram / YouTube URL")
    is_active = models.BooleanField(default=True, verbose_name="Show on Website")

    @property
    def get_embed_url(self):
        if 'instagram.com' in self.url:
            clean_url = self.url.split('?')[0]
            if not clean_url.endswith('/'):
                clean_url += '/'
            return f"{clean_url}embed"
        elif 'youtube.com' in self.url or 'youtu.be' in self.url:
            if 'shorts/' in self.url:
                video_id = self.url.split('shorts/')[1].split('?')[0]
            elif 'watch?v=' in self.url:
                video_id = self.url.split('watch?v=')[1].split('&')[0]
            else:
                video_id = self.url.split('/')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.url

    def __str__(self):
        return f"{self.get_platform_display()} - {self.title}"

class SocialAndAppSettings(models.Model):
    site_name = models.CharField(max_length=100, default="NL Makeover", verbose_name="Salon Name", blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Salon Logo")
    phone_number = models.CharField(max_length=20, verbose_name="WhatsApp / Contact Number", blank=True, null=True)
    whatsapp_channel_url = models.URLField(verbose_name="WhatsApp Channel Link", blank=True, null=True)
    instagram_url = models.URLField(verbose_name="Instagram Profile Link", blank=True, null=True)
    youtube_url = models.URLField(verbose_name="YouTube Channel/Video Link", blank=True, null=True)
    facebook_url = models.URLField(verbose_name="Facebook Page Link", blank=True, null=True)
    google_map_url = models.URLField(verbose_name="Google Map Link (NL Makeover)", blank=True, null=True)
    apk_file = models.FileField(upload_to='apk/', blank=True, null=True, verbose_name="Upload Android APK File")
    address = models.TextField(verbose_name="Salon Address", blank=True, null=True)

    def __str__(self):
        return f"Site & App Settings ({self.site_name})"