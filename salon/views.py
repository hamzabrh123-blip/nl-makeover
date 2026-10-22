from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner, LegalPage, Certificate



def home_view(request):
    banners = SliderBanner.objects.filter(is_active=True).order_by('-id')
    # Home par ab services order/priority ke hisaab se aur sirf top 6 dikhayenge
    services = Service.objects.all()[:6]
    # Home par sirf latest 6 videos dikhayenge
    videos = VideoEmbed.objects.filter(is_active=True).order_by('-id')[:6]
    settings = SocialAndAppSettings.objects.first()
    
    context = {
        'banners': banners,
        'services': services,
        'videos': videos,
        'settings': settings,
    }
    return render(request, 'index.html', context)


def services_list_view(request):
    """Saari services ka dedicated page (templates/services_list.html)"""
    services = Service.objects.all()  # Model ki default ordering ('order', 'id') ke mutabiq aayengi
    settings = SocialAndAppSettings.objects.first()
    context = {
        'services': services,
        'settings': settings,
    }
    return render(request, 'services_list.html', context)



def videos_list_view(request):
    """Saari videos/reels ka dedicated page."""
    videos = VideoEmbed.objects.filter(
        is_active=True
    ).order_by('-id')

    for video in videos:
        print("PLATFORM:", video.platform)
        print("ORIGINAL URL:", video.url)
        print("EMBED URL:", video.get_embed_url)

    settings = SocialAndAppSettings.objects.first()

    context = {
        'videos': videos,
        'settings': settings,
    }

    return render(request, 'salon/videos_list.html', context)


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

def certificates_view(request):
    certificates = Certificate.objects.filter(
        is_active=True
    ).order_by("display_order", "-created_at")

    settings = SocialAndAppSettings.objects.first()

    return render(request, "salon/certificates.html", {
        "certificates": certificates,
        "settings": settings,
    })


def iso_certificate_view(request):
    certificates = Certificate.objects.filter(
        is_active=True,
        title__icontains="ISO"
    ).order_by("display_order", "-created_at")

    settings = SocialAndAppSettings.objects.first()

    return render(request, "salon/certificates/iso.html", {
        "certificates": certificates,
        "settings": settings,
    })


def msme_certificate_view(request):
    certificates = Certificate.objects.filter(
        is_active=True,
        title__icontains="MSME"
    ).order_by("display_order", "-created_at")

    settings = SocialAndAppSettings.objects.first()

    return render(request, "salon/certificates/msme.html", {
        "certificates": certificates,
        "settings": settings,
    })


def academic_certificate_view(request):
    certificates = Certificate.objects.filter(
        is_active=True,
        title__icontains="Academic"
    ).order_by("display_order", "-created_at")

    settings = SocialAndAppSettings.objects.first()

    return render(request, "salon/certificates/academic.html", {
        "certificates": certificates,
        "settings": settings,
    })
def sitemap_view(request):
    services = Service.objects.all()
    videos = VideoEmbed.objects.filter(is_active=True).order_by('-id')
    
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