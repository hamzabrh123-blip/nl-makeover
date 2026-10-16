from django.shortcuts import render
from .models import Service, VideoEmbed, SocialAndAppSettings

def home_view(request):
    services = Service.objects.all()
    videos = VideoEmbed.objects.filter(is_active=True)
    settings = SocialAndAppSettings.objects.first()
    context = {
        'services': services,
        'videos': videos,
        'settings': settings,
    }
    return render(request, 'index.html', context)