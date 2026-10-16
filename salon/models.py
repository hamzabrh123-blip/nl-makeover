from django.db import models


class SliderBanner(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')  # Cloudinary par save hoga
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Banner"


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Service Name")
    category = models.CharField(max_length=100, verbose_name="Category (e.g., Bridal, Hair)")
    price = models.CharField(max_length=50, verbose_name="Price / Starting From")
    description = models.TextField(verbose_name="Service Description")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Service Image") # Cloudinary par save hoga
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
    url = models.URLField(verbose_name="Instagram / YouTube URL (Koi bhi link paste karo)")
    is_active = models.BooleanField(default=True, verbose_name="Show on Website")

    @property
    def get_embed_url(self):
        """
        Smart link parser: Client koi bhi link daale (Shorts, Watch, Reel, Share link),
        yeh function automatic usko embed format mein badal dega.
        """
        if not self.url:
            return ""

        url = self.url.strip()

        # --- INSTAGRAM HANDLING ---
        if 'instagram.com' in url:
            # Clean up query params (jaise ?igsh=...)
            clean_url = url.split('?')[0]
            if not clean_url.endswith('/'):
                clean_url += '/'
            return f"{clean_url}embed"

        # --- YOUTUBE HANDLING ---
        elif 'youtube.com' in url or 'youtu.be' in url:
            video_id = ""
            try:
                if 'shorts/' in url:
                    video_id = url.split('shorts/')[1].split('?')[0].split('/')[0]
                elif 'watch?v=' in url:
                    video_id = url.split('watch?v=')[1].split('&')[0]
                elif 'youtu.be/' in url:
                    video_id = url.split('youtu.be/')[1].split('?')[0].split('/')[0]
                elif 'embed/' in url:
                    video_id = url.split('embed/')[1].split('?')[0].split('/')[0]
                else:
                    video_id = url.split('/')[-1].split('?')[0]
                
                if video_id:
                    return f"https://www.youtube.com/embed/{video_id}"
            except Exception:
                pass
            
            # Fallback agar parsing mein kuch issue ho
            return url

        return url

    def __str__(self):
        return f"{self.get_platform_display()} - {self.title}"


class SocialAndAppSettings(models.Model):
    site_name = models.CharField(max_length=100, default="NL Makeover", verbose_name="Salon Name", blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Salon Logo") # Cloudinary par save hoga
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