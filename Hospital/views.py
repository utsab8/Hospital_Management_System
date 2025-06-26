from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from django.views.decorators.http import require_http_methods

import json
from datetime import datetime, timedelta

from .models import (
    Doctor, Patient, Appointment, Bill, BillItem, 
    Report, Department, Room, MedicalRecord
)

# Dashboard Views
def dashboard(request):
    """Main dashboard with statistics"""
    context = {
        'total_patients': Patient.objects.count(),
        'active_patients': Patient.objects.filter(status='active').count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'today_appointments': Appointment.objects.filter(
            appointment_date=timezone.now().date(),
            status='scheduled'
        ).count(),
        'pending_bills': Bill.objects.filter(status='unpaid').count(),
        'available_rooms': Room.objects.filter(status='available').count(),
        'recent_patients': Patient.objects.all()[:5],
        'todays_appointments': Appointment.objects.filter(
            appointment_date=timezone.now().date()
        ).order_by('appointment_time')[:10],
    }
    return render(request, 'home.html', context)

# Doctor Views
def doctor_list(request):
    """List all doctors with search and filter"""
    doctors = Doctor.objects.filter(is_active=True)
    
    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(license_number__icontains=search_query)
        )
    
    specialty_filter = request.GET.get('specialty')
    if specialty_filter:
        doctors = doctors.filter(specialty=specialty_filter)
    
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    doctors_page = paginator.get_page(page_number)
    
    specialties = [choice[0] for choice in Doctor.SPECIALTY_CHOICES]
    
    context = {
        'doctors': doctors_page,
        'specialties': specialties,
        'search_query': search_query,
        'specialty_filter': specialty_filter,
    }
    return render(request, 'hospital/doctor_list.html', context)

def doctor_detail(request, doctor_id):
    """View doctor details"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    recent_appointments = doctor.appointments.all()[:10]
    patient_count = doctor.patients.filter(status='active').count()
    
    context = {
        'doctor': doctor,
        'recent_appointments': recent_appointments,
        'patient_count': patient_count,
    }
    return render(request, 'hospital/doctor_detail.html', context)

# Patient Views
def patient_list(request):
    """List all patients with search and filter"""
    patients = Patient.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        patients = patients.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(diagnosis__icontains=search_query)
        )
    
    status_filter = request.GET.get('status')
    if status_filter:
        patients = patients.filter(status=status_filter)
    
    paginator = Paginator(patients, 15)
    page_number = request.GET.get('page')
    patients_page = paginator.get_page(page_number)
    
    statuses = [choice[0] for choice in Patient.STATUS_CHOICES]
    
    context = {
        'patients': patients_page,
        'statuses': statuses,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'hospital/patient_list.html', context)

def patient_detail(request, patient_id):
    """View patient details"""
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = patient.appointments.all()[:10]
    bills = patient.bills.all()[:5]
    medical_records = patient.medical_records.all()[:10]
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'bills': bills,
        'medical_records': medical_records,
    }
    return render(request, 'hospital/patient_detail.html', context)

def patient_create(request):
    """Create new patient"""
    if request.method == 'POST':
        try:
            patient = Patient.objects.create(
                name=request.POST['name'],
                age=request.POST['age'],
                gender=request.POST['gender'],
                phone=request.POST['phone'],
                email=request.POST.get('email', ''),
                address=request.POST['address'],
                blood_group=request.POST.get('blood_group', ''),
                emergency_contact=request.POST['emergency_contact'],
                emergency_phone=request.POST['emergency_phone'],
                diagnosis=request.POST['diagnosis'],
                medical_history=request.POST.get('medical_history', ''),
                allergies=request.POST.get('allergies', ''),
                current_medications=request.POST.get('current_medications', ''),
                assigned_doctor_id=request.POST.get('assigned_doctor') or None,
                admitted_date=request.POST['admitted_date'],
            )
            messages.success(request, 'Patient created successfully!')
            return redirect('patient_detail', patient_id=patient.id)
        except Exception as e:
            messages.error(request, f'Error creating patient: {str(e)}')
    
    doctors = Doctor.objects.filter(is_active=True)
    context = {
        'doctors': doctors,
        'gender_choices': Patient.GENDER_CHOICES,
        'blood_group_choices': Patient.BLOOD_GROUP_CHOICES,
        'status_choices': Patient.STATUS_CHOICES,
    }
    return render(request, 'hospital/patient_form.html', context)

# Appointment Views
def appointment_list(request):
    """List appointments with filters"""
    appointments = Appointment.objects.all()
    
    date_filter = request.GET.get('date')
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    
    doctor_filter = request.GET.get('doctor')
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    paginator = Paginator(appointments, 20)
    page_number = request.GET.get('page')
    appointments_page = paginator.get_page(page_number)
    
    doctors = Doctor.objects.filter(is_active=True)
    statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
    
    context = {
        'appointments': appointments_page,
        'doctors': doctors,
        'statuses': statuses,
        'date_filter': date_filter,
        'doctor_filter': doctor_filter,
        'status_filter': status_filter,
    }
    return render(request, 'hospital/appointment_list.html', context)

def appointment_create(request):
    """Create new appointment"""
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.create(
                patient_id=request.POST['patient'],
                doctor_id=request.POST['doctor'],
                appointment_date=request.POST['appointment_date'],
                appointment_time=request.POST['appointment_time'],
                appointment_type=request.POST['appointment_type'],
                duration_minutes=request.POST.get('duration_minutes', 30),
                reason=request.POST['reason'],
                notes=request.POST.get('notes', ''),
            )
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('appointment_list')
        except Exception as e:
            messages.error(request, f'Error creating appointment: {str(e)}')
    
    patients = Patient.objects.filter(status__in=['active', 'admitted'])
    doctors = Doctor.objects.filter(is_active=True)
    
    context = {
        'patients': patients,
        'doctors': doctors,
        'appointment_types': Appointment.APPOINTMENT_TYPE_CHOICES,
    }
    return render(request, 'hospital/appointment_form.html', context)

@require_http_methods(["POST"])
def appointment_update_status(request, appointment_id):
    """Update appointment status via AJAX"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('status')
    
    if new_status in [choice[0] for choice in Appointment.STATUS_CHOICES]:
        appointment.status = new_status
        appointment.save()
        return JsonResponse({'success': True, 'message': 'Status updated successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid status'})

# Bill Views
def bill_list(request):
    """List bills with filters"""
    bills = Bill.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        bills = bills.filter(
            Q(patient__name__icontains=search_query) |
            Q(bill_number__icontains=search_query)
        )
    
    paginator = Paginator(bills, 15)
    page_number = request.GET.get('page')
    bills_page = paginator.get_page(page_number)
    
    statuses = [choice[0] for choice in Bill.STATUS_CHOICES]
    
    context = {
        'bills': bills_page,
        'statuses': statuses,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'hospital/bill_list.html', context)

def bill_detail(request, bill_id):
    """View bill details"""
    bill = get_object_or_404(Bill, id=bill_id)
    bill_items = bill.items.all()
    
    context = {
        'bill': bill,
        'bill_items': bill_items,
    }
    return render(request, 'hospital/bill_detail.html', context)

def bill_create(request):
    """Create new bill"""
    if request.method == 'POST':
        try:
            bill = Bill.objects.create(
                patient_id=request.POST['patient'],
                total_amount=request.POST['total_amount'],
                discount_amount=request.POST.get('discount_amount', 0),
                tax_amount=request.POST.get('tax_amount', 0),
                due_date=request.POST['due_date'],
                description=request.POST.get('description', ''),
            )
            
            items_data = request.POST.get('items_json')
            if items_data:
                items = json.loads(items_data)
                for item in items:
                    BillItem.objects.create(
                        bill=bill,
                        item_type=item['type'],
                        description=item['description'],
                        quantity=item['quantity'],
                        unit_price=item['unit_price'],
                    )
            
            messages.success(request, 'Bill created successfully!')
            return redirect('bill_detail', bill_id=bill.id)
        except Exception as e:
            messages.error(request, f'Error creating bill: {str(e)}')
    
    patients = Patient.objects.all()
    item_types = [choice[0] for choice in BillItem.ITEM_TYPE_CHOICES]
    
    context = {
        'patients': patients,
        'item_types': item_types,
    }
    return render(request, 'hospital/bill_form.html', context)

# Room Views
def room_list(request):
    """List rooms with status"""
    rooms = Room.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        rooms = rooms.filter(status=status_filter)
    
    type_filter = request.GET.get('room_type')
    if type_filter:
        rooms = rooms.filter(room_type=type_filter)
    
    statuses = [choice[0] for choice in Room.STATUS_CHOICES]
    room_types = [choice[0] for choice in Room.ROOM_TYPE_CHOICES]
    
    context = {
        'rooms': rooms,
        'statuses': statuses,
        'room_types': room_types,
        'status_filter': status_filter,
        'type_filter': type_filter,
    }
    return render(request, 'hospital/room_list.html', context)

def room_detail(request, room_id):
    """View room details"""
    room = get_object_or_404(Room, id=room_id)
    
    context = {
        'room': room,
    }
    return render(request, 'hospital/room_detail.html', context)

# Medical Record Views
def medical_record_list(request, patient_id):
    """List medical records for a patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    records = patient.medical_records.all()
    
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    records_page = paginator.get_page(page_number)
    
    context = {
        'patient': patient,
        'records': records_page,
    }
    return render(request, 'hospital/medical_record_list.html', context)

def medical_record_create(request, patient_id):
    """Create new medical record"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        try:
            record = MedicalRecord.objects.create(
                patient=patient,
                doctor_id=request.POST['doctor'],
                visit_date=request.POST['visit_date'],
                symptoms=request.POST['symptoms'],
                diagnosis=request.POST['diagnosis'],
                treatment=request.POST['treatment'],
                prescription=request.POST.get('prescription', ''),
                follow_up_date=request.POST.get('follow_up_date') or None,
                notes=request.POST.get('notes', ''),
            )
            messages.success(request, 'Medical record created successfully!')
            return redirect('medical_record_list', patient_id=patient.id)
        except Exception as e:
            messages.error(request, f'Error creating medical record: {str(e)}')
    
    doctors = Doctor.objects.filter(is_active=True)
    
    context = {
        'patient': patient,
        'doctors': doctors,
    }
    return render(request, 'hospital/medical_record_form.html', context)

# Department Views
def department_list(request):
    """List all departments"""
    departments = Department.objects.filter(is_active=True)
    
    context = {
        'departments': departments,
    }
    return render(request, 'hospital/department_list.html', context)

def department_detail(request, department_id):
    """View department details"""
    department = get_object_or_404(Department, id=department_id)
    rooms = department.rooms.all()
    
    context = {
        'department': department,
        'rooms': rooms,
    }
    return render(request, 'hospital/department_detail.html', context)

# Report Views
def report_list(request):
    """List all reports"""
    reports = Report.objects.all()
    
    type_filter = request.GET.get('report_type')
    if type_filter:
        reports = reports.filter(report_type=type_filter)
    
    report_types = [choice[0] for choice in Report.REPORT_TYPE_CHOICES]
    
    context = {
        'reports': reports,
        'report_types': report_types,
        'type_filter': type_filter,
    }
    return render(request, 'hospital/report_list.html', context)

def generate_revenue_report(request):
    """Generate revenue report"""
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        bills = Bill.objects.filter(
            bill_date__range=[start_date, end_date],
            status='paid'
        )
        
        total_revenue = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_bills = bills.count()
        
        report = Report.objects.create(
            title=f'Revenue Report ({start_date} to {end_date})',
            report_type='revenue',
            summary=f'Total Revenue: ${total_revenue}, Total Bills: {total_bills}',
            generated_by=request.user if request.user.is_authenticated else None,
            report_date=timezone.now().date(),
            period_start=start_date,
            period_end=end_date,
        )
        
        messages.success(request, 'Revenue report generated successfully!')
        return redirect('report_list')
    
    return render(request, 'hospital/generate_report.html', {'report_type': 'revenue'})

# API Views for AJAX requests
def api_patient_search(request):
    """API endpoint for patient search (AJAX)"""
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(
        name__icontains=query
    )[:10]
    
    results = []
    for patient in patients:
        results.append({
            'id': patient.id,
            'name': patient.name,
            'phone': patient.phone,
            'age': patient.age,
        })
    
    return JsonResponse({'results': results})

def api_doctor_availability(request):
    """Check doctor availability for appointment scheduling"""
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    
    if not doctor_id or not date:
        return JsonResponse({'error': 'Missing parameters'})
    
    appointments = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=date,
        status='scheduled'
    ).values_list('appointment_time', flat=True)
    
    available_slots = []
    start_time = datetime.strptime('09:00', '%H:%M').time()
    end_time = datetime.strptime('17:00', '%H:%M').time()
    
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    while current_time <= end_datetime:
        if current_time.time() not in appointments:
            available_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=30)
    
    return JsonResponse({'available_slots': available_slots})
