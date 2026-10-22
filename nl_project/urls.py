from django.contrib import admin
from django.urls import path
from salon.views import (
    certificates_view,
    iso_certificate_view,
    msme_certificate_view,
    academic_certificate_view,
    home_view, 
    sitemap_view, 
    robots_txt_view,
    legal_page_view,
    services_list_view,
    videos_list_view
)
    
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

     # Certificates & Registrations
    path('certificates/', certificates_view, name='certificates'),
    path('certificates/iso/', iso_certificate_view, name='iso_certificate'),
    path('certificates/msme/', msme_certificate_view, name='msme_certificate'),
    path('certificates/academic/', academic_certificate_view, name='academic_certificate'),

    # Dedicated Service & Video Gallery Pages
    path('services/', services_list_view, name='services_list'),
    path('videos/', videos_list_view, name='videos_list'),
    
    # Legal & Compliance Pages (Footer Links ke liye zaroori hain)
    path('about/', legal_page_view, {'slug': 'about'}, name='about'),
    path('contact/', legal_page_view, {'slug': 'contact'}, name='contact'),
    path('privacy-policy/', legal_page_view, {'slug': 'privacy-policy'}, name='privacy_policy'),
    path('terms/', legal_page_view, {'slug': 'terms'}, name='terms'),
    path('disclaimer/', legal_page_view, {'slug': 'disclaimer'}, name='disclaimer'),
    
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)