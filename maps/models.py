from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class PollutedArea(models.Model):
    POLLUTION_TYPES = [
        ('air', 'Air Pollution'),
        ('water', 'Water Pollution'),
        ('soil', 'Soil Pollution'),
        ('noise', 'Noise Pollution'),
        ('light', 'Light Pollution'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        (1, 'Low'),
        (2, 'Moderate'),
        (3, 'High'),
        (4, 'Critical'),
        (5, 'Extreme'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pollution_type = models.CharField(max_length=20, choices=POLLUTION_TYPES)
    severity = models.IntegerField(choices=SEVERITY_LEVELS, validators=[MinValueValidator(1), MaxValueValidator(5)])
    latitude = models.FloatField(help_text="Latitude coordinate")
    longitude = models.FloatField(help_text="Longitude coordinate")
    polygon_coordinates = models.TextField(help_text="Polygon coordinates as JSON", null=True, blank=True)
    area_size = models.FloatField(help_text="Area size in square meters", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polluted_areas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pollution_images/', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Polluted Area'
        verbose_name_plural = 'Polluted Areas'
    
    def get_polygon_coordinates(self):
        """Return polygon coordinates as a list of [lat, lng] pairs"""
        if self.polygon_coordinates:
            try:
                return json.loads(self.polygon_coordinates)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_polygon_coordinates(self, coordinates):
        """Set polygon coordinates from a list of [lat, lng] pairs"""
        if coordinates:
            self.polygon_coordinates = json.dumps(coordinates)
        else:
            self.polygon_coordinates = None
    
    def has_polygon(self):
        """Check if this area has polygon data"""
        return bool(self.polygon_coordinates and self.get_polygon_coordinates())
    
    def __str__(self):
        return f"{self.name} - {self.get_pollution_type_display()}"
    
    @property
    def severity_color(self):
        colors = {
            1: '#28a745',  # Green
            2: '#ffc107',  # Yellow
            3: '#fd7e14',  # Orange
            4: '#dc3545',  # Red
            5: '#6f42c1',  # Purple
        }
        return colors.get(self.severity, '#6c757d')


class PollutionReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('resolved', 'Resolved'),
    ]
    
    polluted_area = models.ForeignKey(PollutedArea, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pollution_reports')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_reports')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report: {self.title} - {self.get_status_display()}"
