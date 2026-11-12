import urllib.request
import json
from math import radians, sin, cos, sqrt, atan2
from django.utils.deprecation import MiddlewareMixin
from .models import VisitorLog

class VisitorTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        
        # Admin, static, aur media files ko track nahi karna
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return None

        # 1. Map exact URL path to our 4 Core Pages
        page_name = None
        if path == '/' or path == '':
            page_name = 'Home'
        elif path.startswith('/offers/'):
            page_name = 'Offers'
        elif path.startswith('/services/') or path.startswith('/service/'):
            page_name = 'Services'
        elif path.startswith('/certificates/academic/'):
            page_name = 'Academic Hub'

        # Agar in 4 core pages ke alawa kisi aur page par gaya, toh log save nahi karna
        if not page_name:
            return None

        # 2. Detect Traffic Platform / Source
        platform = 'Direct Visit'
        
        query_src = request.GET.get('src', '').lower() or request.GET.get('ref', '').lower()
        if 'insta' in query_src:
            platform = 'Instagram'
        elif 'whats' in query_src or 'wa' in query_src:
            platform = 'WhatsApp'
        elif 'face' in query_src or 'fb' in query_src:
            platform = 'Facebook'
        elif 'pin' in query_src:
            platform = 'Pinterest'
        elif 'google' in query_src:
            platform = 'Google Search'
        else:
            referer = request.META.get('HTTP_REFERER', '').lower()
            if 'instagram.com' in referer:
                platform = 'Instagram'
            elif 'whatsapp.com' in referer or 'wa.me' in referer:
                platform = 'WhatsApp'
            elif 'facebook.com' in referer or 'm.facebook.com' in referer:
                platform = 'Facebook'
            elif 'pinterest.com' in referer:
                platform = 'Pinterest'
            elif 'google.com' in referer:
                platform = 'Google Search'
            elif referer:
                platform = 'Direct Visit'

        # 3. Get Real IP Address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')

        # 4. Fetch City & Coordinates via Free Geolocation API with 5km Bahraich Rule
        city_label = 'Bahraich (City)'
        try:
            if ip and ip != '127.0.0.1' and ip != 'localhost':
                url = f"https://ipapi.co/{ip}/json/"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    api_city = data.get('city', '')
                    lat = data.get('latitude')
                    lon = data.get('longitude')

                    if api_city:
                        if api_city.lower() == 'bahraich':
                            # Shop main coordinates (Brahmnipura, Bahraich)
                            shop_lat, shop_lon = 27.5758, 81.5956
                            
                            if lat and lon:
                                distance = self._calculate_distance(shop_lat, shop_lon, float(lat), float(lon))
                                if distance <= 5.0:
                                    city_label = 'Bahraich (City)'
                                else:
                                    city_label = 'Bahraich (Gaon)'
                            else:
                                city_label = 'Bahraich (City)'
                        else:
                            city_label = api_city
            else:
                city_label = 'Bahraich (City)'
        except Exception:
            city_label = 'Bahraich (City)'

        # 5. Save to Database
        VisitorLog.objects.create(
            city=city_label,
            platform=platform,
            page=page_name,
            ip_address=ip if ip else None
        )

        return None

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c