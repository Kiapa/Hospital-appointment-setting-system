from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment, Service, ContactMessage


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'specialization', 'department', 'email', 'is_available']
    search_fields = ['first_name', 'last_name', 'email', 'specialization']
    list_filter = ['specialization', 'department', 'is_available', 'created_at']
    list_editable = ['is_available']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'phone', 'date_of_birth']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_filter = ['gender', 'created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    list_filter = ['status', 'appointment_date', 'department', 'created_at']
    list_editable = ['status']
    date_hierarchy = 'appointment_date'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'price', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['department', 'is_active', 'created_at']
    list_editable = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
