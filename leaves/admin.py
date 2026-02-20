from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'type_conge', 'date_debut', 'date_fin', 'statut', 'created_at']
    list_filter = ['statut', 'type_conge', 'created_at']
    search_fields = ['employee__username', 'employee__email', 'raison']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
