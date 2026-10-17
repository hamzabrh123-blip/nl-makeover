from django.shortcuts import render
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Service

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

def sitemap_view(request):
    services = Service.objects.all()
    
    context = {
        'services': services,
        'request': request,
    }
    xml_content = render_to_string('sitemap.xml', context)
    return HttpResponse(xml_content, content_type="application/xml")