import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner, LegalPage, Certificate
from .offer_models import SpecialOffer


def home_view(request):
    banners = SliderBanner.objects.filter(is_active=True).order_by('display_order', '-id')
    # Sirf active services hi home page par dikhengi
    services = Service.objects.filter(is_active=True)[:6]
    videos = VideoEmbed.objects.filter(is_active=True).order_by('-id')[:6]
    settings = SocialAndAppSettings.objects.first()

    active_offer = SpecialOffer.objects.filter(is_active=True).order_by('-created_at').first()
    if active_offer and active_offer.is_expired():
        active_offer = None

    context = {
        'banners': banners,
        'services': services,
        'videos': videos,
        'settings': settings,
        'active_offer': active_offer,
    }
    return render(request, 'index.html', context)


def offers_page_view(request):
    settings = SocialAndAppSettings.objects.first()

    deal_of_the_day = SpecialOffer.objects.filter(is_active=True, offer_type='daily').order_by('-created_at').first()
    if deal_of_the_day and deal_of_the_day.is_expired():
        deal_of_the_day = None

    weekly_offer = SpecialOffer.objects.filter(is_active=True, offer_type='weekly').order_by('-created_at').first()
    if weekly_offer and weekly_offer.is_expired():
        weekly_offer = None

    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        offer = get_object_or_404(SpecialOffer, id=offer_id)

        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        wa_number = settings.phone_number if settings and settings.phone_number else "919170112725"

        template = getattr(settings, 'manager_wa_template', None)
        if not template:
            template = (
                "🎉 *NL MAKEOVER - SPECIAL OFFER BOOKING* 🎉\n\n"
                "Hi Manager, maine yeh offer claim kiya hai:\n"
                "✨ *Offer:* {offer_title}\n"
                "🏷️ *Discount:* {discount_tag}\n"
                "----------------------------------\n"
                "👤 *Customer Name:* {name}\n"
                "📍 *Address:* {address}\n"
                "📞 *Mobile:* {phone}\n"
                "----------------------------------\n"
                "Kripya meri booking confirm karein!"
            )

        formatted_message = template.format(
            name=name,
            address=address,
            phone=phone,
            offer_title=offer.title,
            discount_tag=offer.discount_tag
        )

        encoded_message = urllib.parse.quote(formatted_message)
        whatsapp_url = f"https://wa.me/{wa_number}?text={encoded_message}"

        return redirect(whatsapp_url)

    context = {
        'deal_of_the_day': deal_of_the_day,
        'weekly_offer': weekly_offer,
        'settings': settings,
    }
    return render(request, 'salon/offer_booking.html', context)


def services_list_view(request):
    """Saari active services ka dedicated page"""
    services = Service.objects.filter(is_active=True)
    settings = SocialAndAppSettings.objects.first()
    context = {
        'services': services,
        'settings': settings,
    }
    return render(request, 'services_list.html', context)


def service_detail_view(request, pk):
    """Purane 1-6 ID links ke liye safe handler"""
    service = get_object_or_404(Service, pk=pk)
    settings = SocialAndAppSettings.objects.first()
    context = {
        'service': service,
        'settings': settings,
    }
    return render(request, 'salon/service_detail.html', context)


def service_detail_slug_view(request, slug):
    """Naye SEO Slug pages ke liye handler"""
    service = get_object_or_404(Service, slug=slug)
    settings = SocialAndAppSettings.objects.first()
    context = {
        'service': service,
        'settings': settings,
    }
    return render(request, 'salon/service_detail.html', context)


def videos_list_view(request):
    videos = VideoEmbed.objects.filter(is_active=True).order_by('-id')
    settings = SocialAndAppSettings.objects.first()
    context = {
        'videos': videos,
        'settings': settings,
    }
    return render(request, 'salon/videos_list.html', context)


def legal_page_view(request, slug):
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
    certificates = Certificate.objects.filter(is_active=True).order_by("display_order", "-created_at")
    settings = SocialAndAppSettings.objects.first()
    return render(request, "salon/certificates.html", {"certificates": certificates, "settings": settings})


def iso_certificate_view(request):
    certificates = Certificate.objects.filter(is_active=True, title__icontains="ISO").order_by("display_order", "-created_at")
    settings = SocialAndAppSettings.objects.first()
    return render(request, "salon/certificates/iso.html", {"certificates": certificates, "settings": settings})


def msme_certificate_view(request):
    certificates = Certificate.objects.filter(is_active=True, title__icontains="MSME").order_by("display_order", "-created_at")
    settings = SocialAndAppSettings.objects.first()
    return render(request, "salon/certificates/msme.html", {"certificates": certificates, "settings": settings})


def academic_certificate_view(request):
    certificates = Certificate.objects.filter(is_active=True, title__icontains="Academic").order_by("display_order", "-created_at")
    settings = SocialAndAppSettings.objects.first()
    return render(request, "salon/certificates/academic.html", {"certificates": certificates, "settings": settings})


def sitemap_view(request):
    # Sirf active services hi sitemap mein jayengi
    services = Service.objects.filter(is_active=True)
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

Sitemap: https://www.nlmakeover.in/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")