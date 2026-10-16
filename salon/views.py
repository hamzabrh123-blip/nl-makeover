from django.shortcuts import render
from .models import Service, VideoEmbed, SocialAndAppSettings, SliderBanner

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