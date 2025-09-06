from django.contrib import admin
from .models import PollutedArea, PollutionReport


@admin.register(PollutedArea)
class PollutedAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'pollution_type', 'severity', 'created_by', 'created_at', 'is_active']
    list_filter = ['pollution_type', 'severity', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Pollution Details', {
            'fields': ('pollution_type', 'severity', 'area_size')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(PollutionReport)
class PollutionReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'polluted_area', 'reporter', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'verified_at']
    search_fields = ['title', 'description', 'reporter__username', 'polluted_area__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'verified_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'description', 'polluted_area', 'reporter')
        }),
        ('Status', {
            'fields': ('status', 'verified_by', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and obj.status == 'verified':
            obj.verified_by = request.user
        super().save_model(request, obj, form, change)
