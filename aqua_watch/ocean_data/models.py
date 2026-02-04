from django.db import models
from django.core.exceptions import ValidationError

def validate_coastal_only(value):
    coastal_terms = ['coast', 'beach', 'bay', 'sea', 'ocean', 'creek', 'harbor', 'port']
    if not any(term in value.lower() for term in coastal_terms):
        raise ValidationError("Please enter a valid coastal area name.")

class MarineRecord(models.Model):
    location = models.CharField(max_length=100, validators=[validate_coastal_only])
    temperature = models.FloatField()
    salinity = models.FloatField(default=35.0) # Added salinity column
    status = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

class SpeciesGrowthCondition(models.Model):
    species_name = models.CharField(max_length=100)
    description = models.TextField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    ideal_ph = models.FloatField()
    salinity_ppt = models.FloatField(default=35.0)
    oxygen_level = models.FloatField(default=6.0)

    def __str__(self):
        return self.species_name
    
class MarineRecord(models.Model):
    location = models.CharField(max_length=100, validators=[validate_coastal_only])
    latitude = models.FloatField(default=19.0760)  # Added for Map
    longitude = models.FloatField(default=72.8777) # Added for Map
    temperature = models.FloatField()
    salinity = models.FloatField(default=35.0)
    status = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)