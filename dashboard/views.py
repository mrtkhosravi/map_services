from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from maps.models import PollutedArea, PollutionReport


@login_required
def dashboard_home(request):
    # Get statistics
    total_areas = PollutedArea.objects.filter(is_active=True).count()
    user_areas = PollutedArea.objects.filter(created_by=request.user, is_active=True).count()
    total_reports = PollutionReport.objects.count()
    user_reports = PollutionReport.objects.filter(reporter=request.user).count()
    
    # Recent areas
    recent_areas = PollutedArea.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Recent reports
    recent_reports = PollutionReport.objects.filter(reporter=request.user).order_by('-created_at')[:5]
    
    # Pollution type distribution
    pollution_stats = PollutedArea.objects.filter(is_active=True).values('pollution_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Severity distribution
    severity_stats = PollutedArea.objects.filter(is_active=True).values('severity').annotate(
        count=Count('id')
    ).order_by('severity')
    
    # Areas created in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_areas_count = PollutedArea.objects.filter(
        created_at__gte=thirty_days_ago,
        is_active=True
    ).count()
    
    context = {
        'total_areas': total_areas,
        'user_areas': user_areas,
        'total_reports': total_reports,
        'user_reports': user_reports,
        'recent_areas': recent_areas,
        'recent_reports': recent_reports,
        'pollution_stats': pollution_stats,
        'severity_stats': severity_stats,
        'recent_areas_count': recent_areas_count,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def my_areas(request):
    areas = PollutedArea.objects.filter(created_by=request.user, is_active=True).order_by('-created_at')
    return render(request, 'dashboard/my_areas.html', {'areas': areas})


@login_required
def my_reports(request):
    reports = PollutionReport.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'dashboard/my_reports.html', {'reports': reports})

