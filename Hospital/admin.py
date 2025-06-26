from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum,Q
from django.utils import timezone
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse
import csv
from django.db import models

from .models import (
    Doctor, Patient, Appointment, Bill, BillItem, 
    Report, Department, Room, MedicalRecord
)

# Custom Admin Actions
def export_to_csv(modeladmin, request, queryset):
    """Export selected records to CSV"""
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name_plural}.csv'
    
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    
    # Write header
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in fields])
    
    return response

export_to_csv.short_description = 'Export selected records to CSV'

# Custom Filters
class ActiveStatusFilter(admin.SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'is_active'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Active'),
            ('no', 'Inactive'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_active=True)
        if self.value() == 'no':
            return queryset.filter(is_active=False)

class OverdueBillFilter(admin.SimpleListFilter):
    title = 'Bill Status'
    parameter_name = 'overdue'
    
    def lookups(self, request, model_admin):
        return (
            ('overdue', 'Overdue'),
            ('paid', 'Paid'),
            ('unpaid', 'Unpaid'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'overdue':
            return queryset.filter(due_date__lt=timezone.now().date(), status='unpaid')
        if self.value() == 'paid':
            return queryset.filter(status='paid')
        if self.value() == 'unpaid':
            return queryset.filter(status='unpaid')

# Inline Admin Classes
class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1
    readonly_fields = ('total_price',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('appointment_date', 'appointment_time', 'appointment_type', 'status', 'notes')

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('visit_date', 'doctor', 'symptoms', 'diagnosis', 'treatment', 'prescription', 'follow_up_date')

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    readonly_fields = ('created_at', 'updated_at')

# Doctor Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone', 'email', 'years_of_experience', 'patient_count_display', 'is_active_display', 'is_active', 'created_at')
    list_filter = ('specialty', ActiveStatusFilter, 'years_of_experience', 'created_at')
    search_fields = ('name', 'email', 'phone', 'license_number', 'specialty')
    readonly_fields = ('created_at', 'updated_at', 'patient_count_display')
    list_editable = ('is_active',)
    list_per_page = 20
    ordering = ('name',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'specialty', 'phone', 'email')
        }),
        ('Professional Details', {
            'fields': ('license_number', 'years_of_experience', 'qualification')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [AppointmentInline]
    actions = [export_to_csv]
    
    def patient_count_display(self, obj):
        count = obj.patient_count
        color = 'green' if count > 10 else 'orange' if count > 5 else 'red'
        return format_html(
            '<span style="color: {};">{} patients</span>',
            color, count
        )
    patient_count_display.short_description = 'Active Patients'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    is_active_display.short_description = 'Status'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            active_patients=Count('patients', filter=models.Q(patients__status='active'))
        )

# Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'phone', 'assigned_doctor', 'status_display', 'status', 'days_admitted_display', 'admitted_date')
    list_filter = ('status', 'gender', 'blood_group', ('admitted_date', DateFieldListFilter), 'assigned_doctor')
    search_fields = ('name', 'phone', 'email', 'diagnosis', 'emergency_contact')
    readonly_fields = ('created_at', 'updated_at', 'days_admitted_display')
    list_editable = ('status',)
    list_per_page = 25
    ordering = ('-admitted_date',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'age', 'gender', 'phone', 'email', 'address', 'blood_group')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Medical Information', {
            'fields': ('diagnosis', 'medical_history', 'allergies', 'current_medications', 'assigned_doctor')
        }),
        ('Admission Details', {
            'fields': ('status', 'admitted_date', 'discharge_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [AppointmentInline, MedicalRecordInline]
    actions = [export_to_csv]
    
    def status_display(self, obj):
        colors = {
            'active': 'green',
            'discharged': 'blue',
            'admitted': 'orange',
            'emergency': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def days_admitted_display(self, obj):
        days = obj.days_admitted
        if days > 30:
            color = 'red'
        elif days > 14:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {};">{} days</span>',
            color, days
        )
    days_admitted_display.short_description = 'Days Admitted'

# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'status_display', 'status', 'duration_minutes')
    list_filter = ('status', 'appointment_type', ('appointment_date', DateFieldListFilter), 'doctor')
    search_fields = ('patient__name', 'doctor__name', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    list_per_page = 30
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'duration_minutes')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [export_to_csv]
    
    def status_display(self, obj):
        colors = {
            'scheduled': 'blue',
            'completed': 'green',
            'cancelled': 'red',
            'rescheduled': 'orange',
            'no_show': 'purple'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'

# Bill Admin
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'patient', 'total_amount', 'paid_amount', 'balance_amount_display', 'status_display', 'status', 'due_date', 'is_overdue_display')
    list_filter = ('status', OverdueBillFilter, ('bill_date', DateFieldListFilter), 'payment_method')
    search_fields = ('bill_number', 'patient__name', 'description')
    readonly_fields = ('bill_number', 'created_at', 'updated_at', 'balance_amount_display', 'is_overdue_display')
    list_editable = ('status',)
    list_per_page = 25
    ordering = ('-bill_date',)
    date_hierarchy = 'bill_date'
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('bill_number', 'patient', 'description')
        }),
        ('Financial Details', {
            'fields': ('total_amount', 'paid_amount', 'discount_amount', 'tax_amount', 'balance_amount_display')
        }),
        ('Payment Information', {
            'fields': ('status', 'payment_method', 'due_date', 'payment_date')
        }),
        ('Status', {
            'fields': ('is_overdue_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [BillItemInline]
    actions = [export_to_csv]
    
    def balance_amount_display(self, obj):
        balance = obj.balance_amount
        if balance > 0:
            return format_html('<span style="color: red; font-weight: bold;">${:.2f}</span>', balance)
        return format_html('<span style="color: green;">$0.00</span>')
    balance_amount_display.short_description = 'Balance'
    
    def status_display(self, obj):
        colors = {
            'paid': 'green',
            'unpaid': 'red',
            'partially_paid': 'orange',
            'overdue': 'purple',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠ OVERDUE</span>')
        return format_html('<span style="color: green;">✓ On Time</span>')
    is_overdue_display.short_description = 'Due Status'

# Bill Item Admin
@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'item_type', 'description', 'quantity', 'unit_price', 'total_price')
    list_filter = ('item_type', 'bill__status')
    search_fields = ('description', 'bill__bill_number', 'bill__patient__name')
    readonly_fields = ('total_price',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields

# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_doctor', 'location', 'phone', 'room_count_display', 'is_active_display', 'is_active')
    list_filter = (ActiveStatusFilter, 'head_doctor')
    search_fields = ('name', 'description', 'location', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at', 'room_count_display')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'description', 'head_doctor')
        }),
        ('Contact Details', {
            'fields': ('location', 'phone', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('room_count_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RoomInline]
    actions = [export_to_csv]
    
    def room_count_display(self, obj):
        count = obj.rooms.count()
        available = obj.rooms.filter(status='available').count()
        return format_html(
            '{} total ({} available)',
            count, available
        )
    room_count_display.short_description = 'Rooms'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    is_active_display.short_description = 'Status'

# Room Admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'department', 'floor', 'status_display', 'status', 'current_patient', 'daily_rate', 'capacity')
    list_filter = ('status', 'room_type', 'department', 'floor')
    search_fields = ('room_number', 'department__name', 'current_patient__name')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    ordering = ('room_number',)
    
    fieldsets = (
        ('Room Information', {
            'fields': ('room_number', 'room_type', 'department', 'floor', 'capacity')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'current_patient')
        }),
        ('Financial', {
            'fields': ('daily_rate',)
        }),
        ('Additional Details', {
            'fields': ('amenities',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [export_to_csv]
    
    def status_display(self, obj):
        colors = {
            'available': 'green',
            'occupied': 'red',
            'maintenance': 'orange',
            'reserved': 'blue'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'

# Medical Record Admin
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'visit_date', 'diagnosis_short', 'follow_up_date', 'created_at')
    list_filter = ('doctor', ('visit_date', DateFieldListFilter), ('follow_up_date', DateFieldListFilter))
    search_fields = ('patient__name', 'doctor__name', 'symptoms', 'diagnosis', 'treatment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-visit_date',)
    date_hierarchy = 'visit_date'
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('patient', 'doctor', 'visit_date')
        }),
        ('Medical Details', {
            'fields': ('symptoms', 'diagnosis', 'treatment', 'prescription')
        }),
        ('Follow-up', {
            'fields': ('follow_up_date', 'notes')
        }),
        ('Attachments', {
            'fields': ('attachments',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [export_to_csv]
    
    def diagnosis_short(self, obj):
        return obj.diagnosis[:50] + '...' if len(obj.diagnosis) > 50 else obj.diagnosis
    diagnosis_short.short_description = 'Diagnosis'

# Report Admin
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'status_display', 'report_date', 'period_display')
    list_filter = ('report_type', 'status', ('report_date', DateFieldListFilter), 'generated_by')
    search_fields = ('title', 'summary', 'report_type')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-report_date',)
    date_hierarchy = 'report_date'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'report_type', 'generated_by', 'status')
        }),
        ('Content', {
            'fields': ('summary', 'detailed_content')
        }),
        ('Period', {
            'fields': ('report_date', 'period_start', 'period_end')
        }),
        ('Attachments', {
            'fields': ('file_attachment',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [export_to_csv]
    
    def status_display(self, obj):
        colors = {
            'draft': 'orange',
            'published': 'green',
            'archived': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def period_display(self, obj):
        if obj.period_start and obj.period_end:
            return f"{obj.period_start} to {obj.period_end}"
        return "Single Date"
    period_display.short_description = 'Period'

# Customize Admin Site
admin.site.site_header = "Hospital Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Welcome to Hospital Management System"