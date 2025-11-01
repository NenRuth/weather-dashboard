from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    
    def __str__(self):
        if self.country:
            return f"{self.name}, {self.country}"
        return self.name

class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.city.name}: {self.temperature}°C"