from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PollutedArea, PollutionReport


class PollutedAreaForm(forms.ModelForm):
    latitude = forms.FloatField(
        label=_('Latitude'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Latitude (e.g., 40.7128)'),
            'step': 'any'
        })
    )
    longitude = forms.FloatField(
        label=_('Longitude'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Longitude (e.g., -74.0060)'),
            'step': 'any'
        })
    )
    
    class Meta:
        model = PollutedArea
        fields = ['name', 'description', 'pollution_type', 'severity', 'latitude', 'longitude', 'area_size', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pollution_type': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'area_size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add hidden field for polygon coordinates
        self.fields['polygon_coordinates'] = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )


class PollutionReportForm(forms.ModelForm):
    class Meta:
        model = PollutionReport
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
