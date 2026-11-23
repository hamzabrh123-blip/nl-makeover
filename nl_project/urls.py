from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
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
    service_detail_view,
    service_detail_slug_view,
    videos_list_view,
    offers_page_view
)
from django.conf import settings
from django.conf.urls.static import static


def ads_txt_view(request):
    content = "google.com, pub-3171847065256414, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    # Special Offers Page Route
    path('offers/', offers_page_view, name='offers_page'),

    # Certificates & Registrations
    path('certificates/', certificates_view, name='certificates'),
    path('certificates/iso/', iso_certificate_view, name='iso_certificate'),
    path('certificates/msme/', msme_certificate_view, name='msme_certificate'),
    path('certificates/academic/', academic_certificate_view, name='academic_certificate'),

    # Dedicated Service Pages (Old PK URL untouched + New Slug URL added)
    path('services/', services_list_view, name='services_list'),
    path('service/<int:pk>/', service_detail_view, name='service_detail'),
    path('service/<slug:slug>/', service_detail_slug_view, name='service_detail_slug'),
    path('videos/', videos_list_view, name='videos_list'),

    # Legal & Compliance Pages
    path('about/', legal_page_view, {'slug': 'about'}, name='about'),
    path('contact/', legal_page_view, {'slug': 'contact'}, name='contact'),
    path('privacy-policy/', legal_page_view, {'slug': 'privacy-policy'}, name='privacy_policy'),
    path('terms/', legal_page_view, {'slug': 'terms'}, name='terms'),
    path('disclaimer/', legal_page_view, {'slug': 'disclaimer'}, name='disclaimer'),

    # SEO & AdSense Verification Files
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('ads.txt', ads_txt_view, name='ads_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)