import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_weather_data(city_name):
    """Fetch weather data from OpenWeatherMap API"""
    # Use OPENWEATHER_API_KEY to match your settings
    API_KEY = getattr(settings, 'OPENWEATHER_API_KEY', '')
    
    if not API_KEY:
        return {
            'success': False, 
            'error': 'API key not configured. Please add OPENWEATHER_API_KEY to settings.py'
        }
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        logger.info(f"API Response for {city_name}: {data}")
        
        if response.status_code == 200:
            return {
                'city': city_name,
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'success': True
            }
        elif response.status_code == 401:
            return {'success': False, 'error': 'Invalid API key'}
        elif response.status_code == 404:
            return {'success': False, 'error': f'City "{city_name}" not found'}
        else:
            return {'success': False, 'error': f'API error: {data.get("message", "Unknown error")}'}
            
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return {'success': False, 'error': f'Network error: {str(e)}'}

def dashboard(request):
    """Main dashboard view"""
    # Start with an empty list - we'll let users search for cities
    weather_data = []
    
    return render(request, 'weather/dashboard.html', {
        'weather_data': weather_data
    })

def search_weather(request):
    """Search for weather in a specific city"""
    city_name = request.GET.get('city', '').strip()
    if city_name:
        data = get_weather_data(city_name)
        return JsonResponse(data)
    return JsonResponse({'success': False, 'error': 'No city provided'})

def temperature_trend(request, city_name):
    """API endpoint for temperature trend data"""
    trend_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'temperatures': [22, 24, 23, 25, 26, 24, 22],
        'city': city_name
    }
    return JsonResponse(trend_data)