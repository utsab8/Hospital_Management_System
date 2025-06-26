from django.urls import path
from . import views

app_name = 'Hospital'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/medical-records/', views.medical_record_list, name='medical_record_list'),
    path('patients/<int:patient_id>/medical-records/create/', views.medical_record_create, name='medical_record_create'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:appointment_id>/update-status/', views.appointment_update_status, name='appointment_update_status'),

    # Billing
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),
    path('bills/<int:bill_id>/', views.bill_detail, name='bill_detail'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),

    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/revenue/generate/', views.generate_revenue_report, name='generate_revenue_report'),

    # AJAX/API
    path('api/patients/search/', views.api_patient_search, name='api_patient_search'),
    path('api/doctors/availability/', views.api_doctor_availability, name='api_doctor_availability'),
]
