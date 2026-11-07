from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField  # <-- CKEditor import kiya

class SpecialOffer(models.Model):
    OFFER_TYPES = (
        ('daily', 'Deal of the Day'),
        ('weekly', 'Weekly Offer'),
    )
    
    title = models.CharField(max_length=255, help_text="Jaise: Grand Bridal Fest - 50% OFF")
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='daily', help_text="Select offer category")
    
    # Description mein ab CKEditor RichTextField lag gaya hai
    description = RichTextField(help_text="Offer ki rich details yahan likhein")
    
    discount_tag = models.CharField(max_length=50, default="LIMITED TIME OFFER")
    image = models.ImageField(upload_to='offers/', blank=True, null=True, help_text="Offer banner image")
    end_time = models.DateTimeField(help_text="Offer kab khatam hoga (Date & Time)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.end_time

    def __str__(self):
        return f"[{self.get_offer_type_display()}] {self.title}"