from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import PollutedArea, PollutionReport
from .forms import PollutedAreaForm, PollutionReportForm

class MapView(LoginRequiredMixin, ListView):
    model = PollutedArea
    template_name = 'maps/map.html'
    context_object_name = 'polluted_areas'
    paginate_by = 20
    login_url = 'core:login'
    
    def get_queryset(self):
        return PollutedArea.objects.filter(is_active=True).select_related('created_by')


@login_required
def add_polluted_area(request):
    if request.method == 'POST':
        form = PollutedAreaForm(request.POST, request.FILES)
        if form.is_valid():
            polluted_area = form.save(commit=False)
            polluted_area.created_by = request.user
            
            # Handle polygon coordinates if provided
            polygon_coords = request.POST.get('polygon_coordinates')
            if polygon_coords:
                try:
                    import json
                    coords = json.loads(polygon_coords)
                    polluted_area.set_polygon_coordinates(coords)
                except (json.JSONDecodeError, TypeError):
                    pass  # Ignore invalid polygon data
            
            polluted_area.save()

            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Polluted area has been successfully added!'})
            else:
                messages.success(request, 'Polluted area has been successfully added!')
                return redirect('maps:map')
        else:
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            else:
                return render(request, 'maps/add_area.html', {'form': form})
    else:
        form = PollutedAreaForm()

    return render(request, 'maps/add_area.html', {'form': form})


@login_required
def edit_polluted_area(request, pk):
    polluted_area = get_object_or_404(PollutedArea, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = PollutedAreaForm(request.POST, request.FILES, instance=polluted_area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Polluted area has been successfully updated!')
            return redirect('maps:map')
    else:
        form = PollutedAreaForm(instance=polluted_area)
    
    return render(request, 'maps/edit_area.html', {'form': form, 'polluted_area': polluted_area})


@login_required
def delete_polluted_area(request, pk):
    polluted_area = get_object_or_404(PollutedArea, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        polluted_area.delete()
        messages.success(request, 'Polluted area has been successfully deleted!')
        return redirect('maps:map')
    
    return render(request, 'maps/delete_area.html', {'polluted_area': polluted_area})


class PollutedAreaDetailView(DetailView):
    model = PollutedArea
    template_name = 'maps/area_detail.html'
    context_object_name = 'polluted_area'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = self.object.reports.all()[:10]
        return context


@login_required
def add_report(request, area_pk):
    polluted_area = get_object_or_404(PollutedArea, pk=area_pk)
    
    if request.method == 'POST':
        form = PollutionReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.polluted_area = polluted_area
            report.reporter = request.user
            report.save()
            messages.success(request, 'Your report has been submitted successfully!')
            return redirect('maps:area_detail', pk=area_pk)
    else:
        form = PollutionReportForm()
    
    return render(request, 'maps/add_report.html', {'form': form, 'polluted_area': polluted_area})


@login_required
def get_polluted_areas_json(request):
    """API endpoint to get polluted areas as GeoJSON"""
    areas = PollutedArea.objects.filter(is_active=True)
    
    features = []
    for area in areas:
        # Determine geometry type based on whether polygon exists
        if area.has_polygon():
            geometry = {
                'type': 'Polygon',
                'coordinates': [area.get_polygon_coordinates()]
            }
        else:
            geometry = {
                'type': 'Point',
                'coordinates': [area.longitude, area.latitude]
            }
        
        features.append({
            'type': 'Feature',
            'geometry': geometry,
            'properties': {
                'id': area.id,
                'name': area.name,
                'pollution_type': area.get_pollution_type_display(),
                'severity': area.severity,
                'severity_color': area.severity_color,
                'description': area.description,
                'created_at': area.created_at.isoformat(),
                'created_by': area.created_by.username,
                'has_polygon': area.has_polygon()
            }
        })
    
    return JsonResponse({
        'type': 'FeatureCollection',
        'features': features
    })
