import requests
from django.conf import settings
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import os

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return round(kelvin - 273.15, 1)


def get_current_weather(city_name):
    """Fetch current weather from OpenWeatherMap API"""
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'temp_min': kelvin_to_celsius(data['main']['temp_min']),
            'temp_max': kelvin_to_celsius(data['main']['temp_max']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'].title(),
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
        }
        return weather_data
    except requests.exceptions.RequestException as e:
        return None


def get_forecast(city_name):
    """Fetch 5-day forecast from OpenWeatherMap API"""
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        forecast_list = []
        for item in data['list'][:40]:  # Get 5 days (40 x 3-hour intervals)
            forecast_list.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temperature': kelvin_to_celsius(item['main']['temp']),
                'humidity': item['main']['humidity'],  # ← This is the UPDATE
                'description': item['weather'][0]['description'].title(),
                'icon': item['weather'][0]['icon'],
            })
        
        return forecast_list
    except requests.exceptions.RequestException as e:
        return None


# ========== CHART GENERATION FUNCTIONS ==========

def create_temperature_trend_chart(forecast_data, city_name):
    """Create 7-day temperature trend line chart"""
    if not forecast_data or len(forecast_data) < 2:
        return None
    
    dates = [item['datetime'].strftime('%m/%d') for item in forecast_data[:7]]
    temps = [item['temperature'] for item in forecast_data[:7]]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linewidth=2, color='#FF6B6B', markersize=8)
    plt.title(f'7-Day Temperature Forecast - {city_name}', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # Save chart
    filename = f'temp_trend_{city_name.replace(" ", "_")}.png'
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f'charts/{filename}'


def create_humidity_chart(forecast_data, city_name):
    """Create humidity bar chart"""
    if not forecast_data or len(forecast_data) < 2:
        return None
    
    dates = [item['datetime'].strftime('%m/%d') for item in forecast_data[:7]]
    humidity = [item.get('humidity', 0) for item in forecast_data[:7]]
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(dates, humidity, color='#4ECDC4', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%', ha='center', va='bottom', fontsize=10)
    
    plt.title(f'7-Day Humidity Levels - {city_name}', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Humidity (%)', fontsize=12)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    filename = f'humidity_{city_name.replace(" ", "_")}.png'
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f'charts/{filename}'


def create_hourly_forecast_chart(forecast_data, city_name):
    """Create 24-hour temperature curve"""
    if not forecast_data or len(forecast_data) < 2:
        return None
    
    hours = [item['datetime'].strftime('%H:%M') for item in forecast_data[:8]]
    temps = [item['temperature'] for item in forecast_data[:8]]
    
    plt.figure(figsize=(12, 5))
    plt.plot(hours, temps, marker='o', linewidth=3, color='#F38181', 
            markersize=10, markerfacecolor='white', markeredgewidth=2)
    plt.fill_between(range(len(hours)), temps, alpha=0.3, color='#F38181')
    
    plt.title(f'24-Hour Temperature Forecast - {city_name}', fontsize=16, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    filename = f'hourly_{city_name.replace(" ", "_")}.png'
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f'charts/{filename}'


def create_multi_city_comparison(cities_data):
    """Compare temperatures across multiple cities"""
    if not cities_data or len(cities_data) < 2:
        return None
    
    plt.figure(figsize=(12, 6))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    for idx, (city_name, forecast) in enumerate(cities_data.items()):
        if forecast and len(forecast) > 0:
            dates = [item['datetime'].strftime('%m/%d') for item in forecast[:7]]
            temps = [item['temperature'] for item in forecast[:7]]
            plt.plot(dates, temps, marker='o', linewidth=2, 
                    label=city_name, color=colors[idx % len(colors)])
    
    plt.title('Temperature Comparison - Multiple Cities', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    filename = 'multi_city_comparison.png'
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f'charts/{filename}'


def create_wind_speed_chart(cities_weather):
    """Compare wind speeds between cities"""
    if not cities_weather or len(cities_weather) < 2:
        return None
    
    cities = list(cities_weather.keys())
    wind_speeds = [data['wind_speed'] for data in cities_weather.values()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cities, wind_speeds, color='#95E1D3', alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} m/s', ha='center', va='bottom', fontsize=10)
    
    plt.title('Wind Speed Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Wind Speed (m/s)', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    filename = 'wind_speed_comparison.png'
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f'charts/{filename}'