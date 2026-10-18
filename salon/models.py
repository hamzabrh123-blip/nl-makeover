import re
from urllib.parse import urlparse, parse_qs
from django.db import models
from ckeditor.fields import RichTextField


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
    description = RichTextField(verbose_name="Service Description")  # CKEditor added here
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Service Image") # Cloudinary par save hoga
    is_featured = models.BooleanField(default=False, verbose_name="Show on Home Page")

    def __str__(self):
        return self.title
    
class VideoEmbed(models.Model):
    PLATFORM_CHOICES = (
        ('youtube', 'YouTube Video / Short'),
        ('instagram', 'Instagram Reel / Post'),
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='youtube',
        verbose_name="Platform"
    )

    title = models.CharField(
        max_length=150,
        verbose_name="Video Title / Caption"
    )

    url = models.URLField(
        verbose_name="Instagram / YouTube URL (Koi bhi link paste karo)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Show on Website"
    )

    @staticmethod
    def _get_youtube_id(url):
        """YouTube video, Shorts aur youtu.be links se video ID nikalo."""
        try:
            parsed = urlparse(url.strip())
            host = (parsed.hostname or '').lower()
            parts = [p for p in parsed.path.split('/') if p]

            video_id = ''

            if host in ('youtu.be', 'www.youtu.be'):
                if parts:
                    video_id = parts[0]

            elif host in (
                'youtube.com',
                'www.youtube.com',
                'm.youtube.com',
                'music.youtube.com',
            ):
                if parsed.path == '/watch':
                    video_id = parse_qs(parsed.query).get('v', [''])[0]

                elif len(parts) >= 2 and parts[0] in (
                    'shorts', 'embed', 'live', 'v'
                ):
                    video_id = parts[1]

            # Standard YouTube video ID: 11 characters.
            if re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id):
                return video_id

        except (ValueError, TypeError):
            pass

        return ''

    @staticmethod
    def _get_instagram_embed_url(url):
        """Public Instagram post/Reel URL ko embed URL mein badlo."""
        try:
            parsed = urlparse(url.strip())
            host = (parsed.hostname or '').lower()

            if host not in (
                'instagram.com',
                'www.instagram.com',
            ):
                return ''

            parts = [p for p in parsed.path.split('/') if p]

            if len(parts) >= 2 and parts[0] in (
                'reel', 'reels', 'p', 'tv'
            ):
                content_type = parts[0]
                shortcode = parts[1]

                if not re.fullmatch(r'[A-Za-z0-9_-]+', shortcode):
                    return ''

                return (
                    f'https://www.instagram.com/'
                    f'{content_type}/{shortcode}/embed/'
                )

        except (ValueError, TypeError):
            pass

        return ''

    @property
    def get_embed_url(self):
        if not self.url:
            return ''

        url = self.url.strip()

        # Platform field ke bajaye URL ko bhi check karte hain,
        # taaki galat platform selection se URL handling na toote.
        youtube_id = self._get_youtube_id(url)
        if youtube_id:
            return f'https://www.youtube.com/embed/{youtube_id}'

        instagram_url = self._get_instagram_embed_url(url)
        if instagram_url:
            return instagram_url

        return ''

    @property
    def get_thumbnail(self):
        """YouTube thumbnail; Instagram thumbnail ke liye alag image chahiye."""
        if not self.url:
            return ''

        youtube_id = self._get_youtube_id(self.url)

        if youtube_id:
            return (
                f'https://img.youtube.com/vi/'
                f'{youtube_id}/hqdefault.jpg'
            )

        return ''

    def __str__(self):
        return f"{self.get_platform_display()} - {self.title}"

class SocialAndAppSettings(models.Model):
    site_name = models.CharField(max_length=100, default="NL Makeover", verbose_name="Salon Name", blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Salon Logo") # Cloudinary par save hoga

    # Naye dynamic fields hero section ke liye:
    hero_tagline = models.CharField(max_length=200, default="Luxury Bridal Studio & Beauty Parlour", blank=True, null=True)
    hero_title = models.CharField(max_length=200, default="Redefining Your Elegance", blank=True, null=True)
    hero_description = RichTextField(default="Step into a world of glamour. Experience professional bridal makeup, high-end hair styling, and premium skin treatments tailored just for you.", blank=True, null=True) # CKEditor added here

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


class LegalPage(models.Model):
    PAGE_CHOICES = (
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
        ('privacy-policy', 'Privacy Policy'),
        ('terms', 'Terms & Conditions'),
        ('disclaimer', 'Disclaimer'),
    )
    
    slug = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, help_text="Select page type")
    title = models.CharField(max_length=200, help_text="Heading of the page")
    content = RichTextField(help_text="Detailed HTML/Text content for this page")  # CKEditor added here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_slug_display()

    class Meta:
        verbose_name = "Legal & Compliance Page"
        verbose_name_plural = "Legal & Compliance Pages"