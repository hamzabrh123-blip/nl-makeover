from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner, LegalPage


def home_view(request):
    banners = SliderBanner.objects.filter(is_active=True)
    services = Service.objects.all()
    videos = VideoEmbed.objects.filter(is_active=True)
    settings = SocialAndAppSettings.objects.first()
    
    context = {
        'banners': banners,
        'services': services,
        'videos': videos,
        'settings': settings,
    }
    return render(request, 'index.html', context)


def legal_page_view(request, slug):
    # Django Admin se fetch karega, agar wahan entry nahi hai toh default fallback dikhayega
    page = LegalPage.objects.filter(slug=slug).first()
    
    default_contents = {
        'about': {
            'title': 'About Us',
            'content': 'Welcome to NL Makeover, your premier destination for professional beauty, grooming, and luxury bridal makeover services in Bahraich, UP.'
        },
        'contact': {
            'title': 'Contact Us',
            'content': 'Have questions or want to book an appointment? Get in touch with NL Makeover.'
        },
        'privacy-policy': {
            'title': 'Privacy Policy',
            'content': 'At NL Makeover (https://nlmakeover.in), the privacy of our visitors is extremely important to us.'
        },
        'terms': {
            'title': 'Terms & Conditions',
            'content': 'Welcome to NL Makeover! These terms and conditions outline the rules and regulations for the use of our website.'
        },
        'disclaimer': {
            'title': 'Disclaimer',
            'content': 'All information on https://nlmakeover.in is published in good faith and for general information purpose only.'
        }
    }

    if not page and slug in default_contents:
        page = {
            'title': default_contents[slug]['title'],
            'content': default_contents[slug]['content']
        }
    elif not page:
        page = {
            'title': 'Page Not Found',
            'content': 'The requested legal page could not be found.'
        }

    return render(request, 'legal_page.html', {'page': page, 'slug': slug})


def sitemap_view(request):
    services = Service.objects.all()
    videos = VideoEmbed.objects.filter(is_active=True)
    
    context = {
        'services': services,
        'videos': videos,
        'request': request,
    }
    xml_content = render_to_string('sitemap.xml', context)
    return HttpResponse(xml_content, content_type="application/xml")


def robots_txt_view(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://nlmakeover.in/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")