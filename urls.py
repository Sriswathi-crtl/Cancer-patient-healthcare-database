from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # LOGIN
    # =========================
    path(
        "login/",
        views.doctor_login,
        name="login"
    ),

    # =========================
    # ADMIN DASHBOARD
    # =========================
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # =========================
    # DOCTOR MANAGEMENT
    # =========================
    path(
        "create-doctor/",
        views.create_doctor,
        name="create_doctor"
    ),

    path(
        "view-doctors/",
        views.view_doctors,
        name="view_doctors"
    ),

    path(
        "edit-doctor/<int:id>/",
        views.edit_doctor,
        name="edit_doctor"
    ),

    path(
        "delete-doctor/<int:id>/",
        views.delete_doctor,
        name="delete_doctor"
    ),

    # =========================
    # PATIENT MANAGEMENT
    # =========================
    path(
        "create-patient/",
        views.create_patient,
        name="create_patient"
    ),

    path(
        "view-patients/",
        views.view_patients,
        name="view_patients"
    ),

    path(
        "edit-patient/<int:id>/",
        views.edit_patient,
        name="edit_patient"
    ),

    path(
        "delete-patient/<int:id>/",
        views.delete_patient,
        name="delete_patient"
    ),

    # =========================
    # USER MANAGEMENT
    # =========================
    path(
        "view-users/",
        views.view_users,
        name="view_users"
    ),

    path(
        "delete-user/<int:id>/",
        views.delete_user,
        name="delete_user"
    ),

    # =========================
    # DOCTOR DASHBOARD
    # =========================
    path(
        "doctor-dashboard/",
        views.doctor_dashboard,
        name="doctor_dashboard"
    ),

    # =========================
    # MY PATIENTS
    # =========================
    path(
        "my-patients/",
        views.my_patients,
        name="my_patients"
    ),
    path(
    "patient-records/",
    views.patient_records,
    name="patient_records"
),

    # =========================
    # PATIENT ASSIGNMENT
    # =========================
    path(
        "assign-patient/",
        views.assign_patient,
        name="assign_patient"
    ),

    path(
        "view-assignments/",
        views.view_assignments,
        name="view_assignments"
    ),

    path(
        "delete-assignment/<int:id>/",
        views.delete_assignment,
        name="delete_assignment"
    ),

    # =========================
    # TREATMENT
    # =========================
    path(
        "add-treatment/",
        views.add_treatment,
        name="add_treatment"
    ),

    path(
        "treatment-history/",
        views.treatment_history,
        name="treatment_history"
    ),

    path(
        "edit-treatment/<int:id>/",
        views.edit_treatment,
        name="edit_treatment"
    ),

    path(
        "delete-treatment/<int:id>/",
        views.delete_treatment,
        name="delete_treatment"
    ),

    # =========================
    # PATIENT RECORD
    # =========================
    path(
        "patient-record/<int:patient_id>/",
        views.view_patient_record,
        name="view_patient_record"
    ),

    # =========================
    # NOTIFICATIONS
    # =========================
    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    path(
        "mark-notification-read/<int:id>/",
        views.mark_notification_read,
        name="mark_notification_read"
    ),

    path(
        "mark-all-notifications-read/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read"
    ),

    path(
        "delete-notification/<int:id>/",
        views.delete_notification,
        name="delete_notification"
    ),

    # =========================
    # PATIENT DASHBOARD
    # =========================
    path(
        "patient-dashboard/",
        views.patient_dashboard,
        name="patient_dashboard"
    ),
    path('patient-profile/', views.patient_profile, name='patient_profile'),
    path('my-doctor/', views.my_doctor, name='my_doctor'),
    path('patient-appointments/', views.patient_appointments, name='patient_appointments'),
    path('patient-treatment/', views.patient_treatment, name='patient_treatment'),
    path(
    'patient-medical-records/',
    views.patient_medical_records,
    name='patient_medical_records'
),
path(
    'patient-prescriptions/',
    views.patient_prescriptions,
    name='patient_prescriptions'
),
path(
    "add-medical-record/",
    views.add_medical_record,
    name="add_medical_record"
),
path(
    'patient-notifications/',
    views.patient_notifications,
    name='patient_notifications'
),
path(
    "doctor-appointments/",
    views.doctor_appointments,
    name="doctor_appointments"
),
]