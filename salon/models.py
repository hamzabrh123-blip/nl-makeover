import re
from urllib.parse import urlparse, parse_qs
from django.db import models
from ckeditor.fields import RichTextField

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    certificate_number = models.CharField(
        max_length=150, blank=True
    )
    issuing_authority = models.CharField(
        max_length=200, blank=True
    )
    issue_date = models.DateField(
        null=True, blank=True
    )
    expiry_date = models.DateField(
        null=True, blank=True
    )
    description = RichTextField(blank=True)
    certificate_file = models.FileField(
        upload_to="certificates/"
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title


class SliderBanner(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name="Banner Title")
    image = models.ImageField(upload_to='banners/', verbose_name="Banner Image")
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Banner Image Alt Text (SEO)"
    )
    service = models.ForeignKey(
        'Service',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Link to Service Page (Dropdown se select karein)"
    )
    custom_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Custom Link (Optional - Agar service select nahi ki toh ye chalega)"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Slide Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        ordering = ['display_order', '-id']

    @property
    def get_target_url(self):
        # 1. Agar service linked hai toh uska clean slug URL do
        if self.service:
            if self.service.slug:
                return f"/service/{self.service.slug}/"
            return f"/service/{self.service.id}/"
        # 2. Warna custom URL do
        if self.custom_url:
            return self.custom_url
        # 3. Kuch bhi set nahi hai toh default services page par bhejo
        return "/services/"

    def save(self, *args, **kwargs):
        if not self.alt_text:
            if self.service:
                self.alt_text = f"{self.service.title} in Bahraich - NL Makeover"
            elif self.title:
                self.alt_text = f"{self.title} - NL Makeover Bahraich"
            else:
                self.alt_text = "NL Makeover Beauty Parlour in Bahraich"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or (self.service.title if self.service else "Banner")


class Service(models.Model):
    CATEGORY_CHOICES = (
        ('Makeup & Styling', 'Makeup & Styling'),
        ('Hair Treatments', 'Hair Treatments'),
        ('Facial & Skin Care', 'Facial & Skin Care'),
        ('Grooming', 'Grooming'),
        ('Other Services', 'Other Services & Academy'),
    )

    title = models.CharField(max_length=200, verbose_name="Service Name (H1)")
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        null=True,
        verbose_name="SEO URL Slug (e.g., bridal-makeup-artist-in-bahraich)"
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Makeup & Styling',
        verbose_name="Service Category"
    )
    price = models.CharField(max_length=50, blank=True, verbose_name="Price / Starting From")
    description = RichTextField(verbose_name="Detailed Service Description")
    
    # Image & Required Alt Text
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Original Service Image")
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Image Alt Text (e.g., Bridal Makeup Artist in Bahraich - NL Makeover)"
    )

    # Dedicated SEO Meta Fields
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="SEO Meta Title (Max 60-70 chars)"
    )
    meta_description = models.TextField(
        max_length=320,
        blank=True,
        verbose_name="SEO Meta Description (Max 155-160 chars)"
    )

    is_active = models.BooleanField(default=True, verbose_name="Active / Show on Website")
    is_featured = models.BooleanField(default=False, verbose_name="Show on Home Page")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order (1, 2, 3)")

    def save(self, *args, **kwargs):
        # Nayi service ke liye slug automatic banega agar khali chhoda
        if not self.slug:
            base_slug = slugify(f"{self.title}-in-bahraich")
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Alt text aur Meta Title khali ho toh automatic fill ho jayega
        if not self.image_alt:
            self.image_alt = f"{self.title} in Bahraich - NL Makeover"
        if not self.meta_title:
            self.meta_title = f"{self.title} in Bahraich | NL Makeover"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.category}] {self.title}"

    class Meta:
        ordering = ['order', 'id']
    
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

class Offer(models.Model):
    OFFER_TYPE_CHOICES = (
        ('weekly', 'Weekly Offer'),
        ('deal', 'Deal of the Day'),
    )

    offer_type = models.CharField(
        max_length=20, 
        choices=OFFER_TYPE_CHOICES, 
        default='deal',
        verbose_name="Offer Type"
    )
    title = models.CharField(max_length=150, verbose_name="Offer Title (e.g., Bridal Glow Week)")
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name="Subtitle / Discount Text (e.g., Flat 25% OFF)")
    original_price = models.CharField(max_length=50, blank=True, null=True, verbose_name="Original Price (Optional)")
    discount_price = models.CharField(max_length=50, blank=True, null=True, verbose_name="Offer / Deal Price (Optional)")
    description = RichTextField(blank=True, null=True, verbose_name="Offer Details")
    banner_image = models.ImageField(upload_to='offers/', blank=True, null=True, verbose_name="Offer Banner / Image")
    valid_till = models.CharField(max_length=100, blank=True, null=True, verbose_name="Validity Text (e.g., Sunday 11:59 PM / Today Only)")
    is_active = models.BooleanField(default=True, verbose_name="Show on Website")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    def __str__(self):
        return f"[{self.get_offer_type_display()}] {self.title}"

    class Meta:
        ordering = ['display_order', '-id']

class SocialAndAppSettings(models.Model):
    site_name = models.CharField(max_length=100, default="NL Makeover", verbose_name="Salon Name", blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Salon Logo")

    # Hero section fields
    hero_tagline = models.CharField(max_length=200, default="Luxury Bridal Studio & Beauty Parlour", blank=True, null=True)
    hero_title = models.CharField(max_length=200, default="NL Makeover – Beauty Parlour in Bahraich", blank=True, null=True)
    hero_description = RichTextField(default="Step into a world of glamour. Experience professional bridal makeup, high-end hair styling, and premium skin treatments tailored just for you.", blank=True, null=True)

    # Homepage / Global Default SEO Fields (Admin se control karne ke liye)
    meta_title = models.CharField(
        max_length=200,
        default="NL Makeover – Best Beauty Parlour in Bahraich | Bridal Makeup & Hair Treatments",
        verbose_name="Website Meta Title (Homepage)",
        blank=True,
        null=True
    )
    meta_description = models.TextField(
        max_length=320,
        default="NL Makeover Bahraich offers bridal makeup, party makeup, hair spa, hair Botox, keratin, Hydra Facial, skin treatments and professional beauty services. Contact us for appointments.",
        verbose_name="Website Meta Description (Homepage)",
        blank=True,
        null=True
    )
    meta_keywords = models.TextField(
        default="Beauty Parlour in Bahraich, Bridal Makeup Artist in Bahraich, Hair Botox in Bahraich, Hair Spa in Bahraich, Keratin Treatment in Bahraich, Hydra Facial in Bahraich, Hair Color in Bahraich, Party Makeup in Bahraich, Beauty Academy in Bahraich, NL Makeover",
        verbose_name="Website Meta Keywords (Comma separated)",
        blank=True,
        null=True
    )

    # Contact & Social Links
    phone_number = models.CharField(max_length=20, verbose_name="WhatsApp / Contact Number", blank=True, null=True)
    whatsapp_channel_url = models.URLField(verbose_name="WhatsApp Channel Link", blank=True, null=True)
    instagram_url = models.URLField(verbose_name="Instagram Profile Link", blank=True, null=True)
    youtube_url = models.URLField(verbose_name="YouTube Channel/Video Link", blank=True, null=True)
    facebook_url = models.URLField(verbose_name="Facebook Page Link", blank=True, null=True)
    google_map_url = models.URLField(verbose_name="Google Map Link (NL Makeover)", blank=True, null=True)
    apk_file = models.FileField(upload_to='apk/', blank=True, null=True, verbose_name="Upload Android APK File")
    address = models.TextField(default="Court Road, Bahraich, Uttar Pradesh – 271801", verbose_name="Salon Address", blank=True, null=True)

    def __str__(self):
        return f"Site & App Settings ({self.site_name})"

class LegalPage(models.Model):
    PAGE_CHOICES = (
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
        ('privacy-pattern', 'Privacy Policy'),
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


class VisitorLog(models.Model):
    PLATFORM_CHOICES = [
        ('Google Search', 'Google Search'),
        ('Instagram', 'Instagram'),
        ('WhatsApp', 'WhatsApp'),
        ('Pinterest', 'Pinterest'),
        ('Facebook', 'Facebook'),
        ('Direct Visit', 'Direct Visit'),
    ]

    PAGE_CHOICES = [
        ('Home', 'Home Page'),
        ('Academic Hub', 'Academic Hub'),
        ('Offers', 'Offers'),
        ('Services', 'Services'),
    ]

    city = models.CharField(max_length=100, verbose_name="Location / City")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='Direct Visit', verbose_name="Platform / Source")
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, verbose_name="Page Visited")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name="Date & Time")

    class Meta:
        verbose_name = "Visitor Log"
        verbose_name_plural = "GPS & Visitor Hub"
        ordering = ['-visited_at']

    def __str__(self):
        return f"{self.city} | {self.platform} -> {self.page}"