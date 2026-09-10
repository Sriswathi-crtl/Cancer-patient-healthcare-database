from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    User,
    Doctor,
    Patient,
    PatientDoctorAssignment,
    Treatment,
    Notification,
    Appointment,
    MedicalRecord
)

from .forms import (
    DoctorForm,
    PatientForm,
    PatientDoctorAssignmentForm,
    TreatmentForm,
    AppointmentForm, 
    MedicalRecordForm
)


# =========================================================
# LOGIN
# =========================================================
def doctor_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:

            user = User.objects.get(
                username=username
            )

            # Check password
            if user.password == password:

                # =================================================
                # ADMIN LOGIN
                # =================================================
                if user.user_type == "ADMIN":

                    request.session["username"] = user.username
                    request.session["user_type"] = "ADMIN"

                    return redirect(
                        "admin_dashboard"
                    )

                # =================================================
                # DOCTOR LOGIN
                # =================================================
                elif user.user_type == "DOCTOR":

                    request.session["doctor_username"] = user.username
                    request.session["user_type"] = "DOCTOR"

                    return redirect(
                        "doctor_dashboard"
                    )

                # =================================================
                # PATIENT LOGIN
                # =================================================
                elif user.user_type == "PATIENT":

                    request.session["username"] = user.username
                    request.session["user_type"] = "PATIENT"

                    request.session.modified = True

                    return redirect(
                        "patient_dashboard"
                    )

            else:

                return render(
                    request,
                    "login.html",
                    {
                        "error": "Invalid password."
                    }
                )

        except User.DoesNotExist:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username."
                }
            )

    return render(
        request,
        "login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================
def admin_dashboard(request):

    doctor_count = Doctor.objects.count()

    patient_count = Patient.objects.count()

    user_count = User.objects.count()

    return render(
        request,
        "admin_dashboard.html",
        {
            "doctor_count": doctor_count,
            "patient_count": patient_count,
            "user_count": user_count,
        }
    )


# =========================================================
# CREATE DOCTOR
# =========================================================
def create_doctor(request):

    if request.method == "POST":

        form = DoctorForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "admin_dashboard"
            )

    else:

        form = DoctorForm()

    return render(
        request,
        "create_doctor.html",
        {
            "form": form
        }
    )


# =========================================================
# VIEW DOCTORS
# =========================================================
def view_doctors(request):

    doctors = Doctor.objects.all()

    return render(
        request,
        "view_doctors.html",
        {
            "doctors": doctors
        }
    )


# =========================================================
# EDIT DOCTOR
# =========================================================
def edit_doctor(request, id):

    doctor = get_object_or_404(
        Doctor,
        id=id
    )

    old_password = doctor.password

    if request.method == "POST":

        form = DoctorForm(
            request.POST,
            instance=doctor
        )

        if form.is_valid():

            doctor = form.save(
                commit=False
            )

            if not doctor.password:

                doctor.password = old_password

            doctor.save()

            return redirect(
                "view_doctors"
            )

    else:

        form = DoctorForm(
            instance=doctor
        )

    return render(
        request,
        "edit_doctor.html",
        {
            "form": form,
            "doctor": doctor
        }
    )


# =========================================================
# DELETE DOCTOR
# =========================================================
def delete_doctor(request, id):

    doctor = get_object_or_404(
        Doctor,
        id=id
    )

    doctor.delete()

    return redirect(
        "view_doctors"
    )


# =========================================================
# CREATE PATIENT
# =========================================================
def create_patient(request):

    if request.method == "POST":

        form = PatientForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "view_patients"
            )

    else:

        form = PatientForm()

    return render(
        request,
        "create_patient.html",
        {
            "form": form
        }
    )


# =========================================================
# VIEW PATIENTS
# =========================================================
def view_patients(request):

    patients = Patient.objects.all()

    return render(
        request,
        "view_patients.html",
        {
            "patients": patients
        }
    )


# =========================================================
# EDIT PATIENT
# =========================================================
def edit_patient(request, id):

    patient = get_object_or_404(
        Patient,
        id=id
    )

    old_username = patient.username

    old_password = patient.password

    old_user = User.objects.filter(
        username=old_username,
        user_type="PATIENT"
    ).first()

    if not old_password and old_user:

        old_password = old_user.password

    if request.method == "POST":

        patient.name = request.POST.get(
            "name"
        )

        patient.email = request.POST.get(
            "email"
        )

        patient.phone = request.POST.get(
            "phone"
        )

        patient.username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        if password and password.strip():

            patient.password = password.strip()

        else:

            patient.password = old_password

        if not patient.password:

            return render(
                request,
                "edit_patient.html",
                {
                    "patient": patient,
                    "error": "Password cannot be empty. Please enter a password."
                }
            )

        patient.save()

        # Notify assigned doctors
        assignments = PatientDoctorAssignment.objects.filter(
            patient=patient
        )

        for assignment in assignments:

            Notification.objects.create(
                doctor=assignment.doctor,
                message=f"Patient {patient.name}'s record has been updated."
            )

        return redirect(
            "view_patients"
        )

    return render(
        request,
        "edit_patient.html",
        {
            "patient": patient
        }
    )


# =========================================================
# DELETE PATIENT
# =========================================================
def delete_patient(request, id):

    patient = get_object_or_404(
        Patient,
        id=id
    )

    patient.delete()

    return redirect(
        "view_patients"
    )


# =========================================================
# DOCTOR DASHBOARD
# =========================================================
def doctor_dashboard(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    assignments = PatientDoctorAssignment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient"
    )

    patient_count = assignments.count()

    active_treatment_count = Treatment.objects.filter(
        doctor=doctor,
        status="ACTIVE"
    ).count()

    notification_count = Notification.objects.filter(
        doctor=doctor,
        is_read=False
    ).count()

    latest_notifications = Notification.objects.filter(
        doctor=doctor
    ).order_by(
        "-created_at"
    )[:3]

    return render(
        request,
        "doctor_dashboard.html",
        {
            "doctor": doctor,
            "assignments": assignments,
            "patient_count": patient_count,
            "active_treatment_count": active_treatment_count,
            "notification_count": notification_count,
            "latest_notifications": latest_notifications,
        }
    )


# =========================================================
# DOCTOR NOTIFICATIONS
# =========================================================
def notifications(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    notifications = Notification.objects.filter(
        doctor=doctor
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "accounts/notifications.html",
        {
            "doctor": doctor,
            "notifications": notifications,
        }
    )


# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================
def mark_notification_read(request, id):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    notification = get_object_or_404(
        Notification,
        id=id,
        doctor=doctor
    )

    notification.is_read = True

    notification.save()

    return redirect(
        "notifications"
    )


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================
def mark_all_notifications_read(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    Notification.objects.filter(
        doctor=doctor,
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        "notifications"
    )


# =========================================================
# DELETE NOTIFICATION
# =========================================================
def delete_notification(request, id):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    notification = get_object_or_404(
        Notification,
        id=id,
        doctor=doctor
    )

    notification.delete()

    return redirect(
        "notifications"
    )


# =========================================================
# MY PATIENTS - DOCTOR
# =========================================================
def my_patients(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    assignments = PatientDoctorAssignment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient"
    )

    return render(
        request,
        "my_patients.html",
        {
            "doctor": doctor,
            "assignments": assignments,
        }
    )


# =========================================================
# PATIENT RECORDS - DOCTOR
# =========================================================
def patient_records(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    assignments = PatientDoctorAssignment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient"
    ).order_by(
        "-assigned_date"
    )

    return render(
        request,
        "patient_records.html",
        {
            "doctor": doctor,
            "assignments": assignments,
        }
    )


# =========================================================
# PATIENT DASHBOARD
# =========================================================
def patient_dashboard(request):

    username = request.session.get(
        "username"
    )

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:

        return redirect(
            "login"
        )

    return render(
        request,
        "patient_dashboard.html",
        {
            "patient": patient
        }
    )


# =========================================================
# PATIENT PROFILE
# =========================================================
def patient_profile(request):

    username = request.session.get(
        "username"
    )

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:

        return redirect(
            "login"
        )

    return render(
        request,
        "patient_profile.html",
        {
            "patient": patient
        }
    )


# =========================================================
# MY DOCTOR - PATIENT
# =========================================================
def my_doctor(request):

    username = request.session.get(
        "username"
    )

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:

        return redirect(
            "login"
        )

    assignments = PatientDoctorAssignment.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-assigned_date"
    )

    return render(
        request,
        "my_doctor.html",
        {
            "patient": patient,
            "assignments": assignments,
        }
    )


# =========================================================
# PATIENT APPOINTMENTS
# =========================================================
def patient_appointments(request):

    username = request.session.get("username")

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:
        return redirect("login")

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.patient = patient

            appointment.status = "SCHEDULED"

            appointment.save()

            return redirect("patient_appointments")

    else:

        form = AppointmentForm()

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    return render(
        request,
        "patient_appointments.html",
        {
            "form": form,
            "appointments": appointments,
            "patient": patient,
        }
    ) 

    # =====================================================
    # BOOK NEW APPOINTMENT
    # =====================================================

    if request.method == "POST":

        form = AppointmentForm(
            request.POST
        )

        if form.is_valid():

            appointment = form.save(
                commit=False
            )

            # Automatically assign logged-in patient
            appointment.patient = patient

            # New appointment is always scheduled
            appointment.status = "SCHEDULED"

            appointment.save()

            return redirect(
                "patient_appointments"
            )

    else:

        form = AppointmentForm()

    # =====================================================
    # PATIENT FIELD
    # =====================================================

    if "patient" in form.fields:

        form.fields["patient"].queryset = Patient.objects.filter(
            id=patient.id
        )

        form.fields["patient"].initial = patient.id

    # =====================================================
    # PATIENT APPOINTMENT HISTORY
    # =====================================================

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    return render(
        request,
        "patient_appointments.html",
        {
            "form": form,
            "appointments": appointments,
            "patient": patient,
        }
    )



# =========================
# PATIENT TREATMENT
# =========================
def patient_treatment(request):

    username = request.session.get("username")

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:
        return redirect("login")

    treatments = Treatment.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-treatment_date"
    )

    return render(
        request,
        "patient_treatment.html",
        {
            "patient": patient,
            "treatments": treatments,
        }
    )



# =========================================================
# PATIENT MEDICAL RECORDS
# =========================================================
def patient_medical_records(request):

    username = request.session.get("username")

    patient = Patient.objects.filter(
        username=username
    ).first()

    if not patient:
        return redirect("login")

    medical_records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-record_date"
    )

    return render(
        request,
        "patient_medical_records.html",
        {
            "patient": patient,
            "medical_records": medical_records,
        }
    )


# =========================================================
# PATIENT PRESCRIPTIONS
# =========================================================
def patient_prescriptions(request):

    return render(
        request,
        "patient_prescriptions.html"
    )


# =========================================================
# PATIENT NOTIFICATIONS
# =========================================================
def patient_notifications(request):

    return render(
        request,
        "patient_notifications.html"
    )


# =========================================================
# VIEW ALL USERS
# =========================================================
def view_users(request):

    admin_users = User.objects.filter(
        user_type="ADMIN"
    ).order_by(
        "id"
    )

    doctor_users = User.objects.filter(
        user_type="DOCTOR"
    ).order_by(
        "id"
    )

    patient_users = User.objects.filter(
        user_type="PATIENT"
    ).order_by(
        "id"
    )

    return render(
        request,
        "view_users.html",
        {
            "admin_users": admin_users,
            "doctor_users": doctor_users,
            "patient_users": patient_users,
        }
    )


# =========================================================
# DELETE USER
# =========================================================
def delete_user(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    username = user.username

    user_type = user.user_type

    user.delete()

    if user_type == "PATIENT":

        Patient.objects.filter(
            username=username
        ).delete()

    elif user_type == "DOCTOR":

        Doctor.objects.filter(
            username=username
        ).delete()

    return redirect(
        "view_users"
    )


# =========================================================
# ASSIGN PATIENT
# =========================================================
def assign_patient(request):

    if request.method == "POST":

        form = PatientDoctorAssignmentForm(
            request.POST
        )

        if form.is_valid():

            assignment = form.save()

            doctor = assignment.doctor

            patient = assignment.patient

            Notification.objects.create(
                doctor=doctor,
                message=f"Patient {patient.name} has been assigned to you."
            )

            return redirect(
                "view_assignments"
            )

    else:

        form = PatientDoctorAssignmentForm()

    return render(
        request,
        "assign_patient.html",
        {
            "form": form
        }
    )


# =========================================================
# VIEW ASSIGNMENTS
# =========================================================
def view_assignments(request):

    assignments = PatientDoctorAssignment.objects.all().order_by(
        "-assigned_date"
    )

    return render(
        request,
        "view_assignments.html",
        {
            "assignments": assignments
        }
    )


# =========================================================
# DELETE ASSIGNMENT
# =========================================================
def delete_assignment(request, id):

    assignment = get_object_or_404(
        PatientDoctorAssignment,
        id=id
    )

    assignment.delete()

    return redirect(
        "view_assignments"
    )


# =========================================================
# ADD TREATMENT
# =========================================================
def add_treatment(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    if request.method == "POST":

        form = TreatmentForm(
            request.POST
        )

        if form.is_valid():

            treatment = form.save(
                commit=False
            )

            treatment.doctor = doctor

            treatment.save()

            Notification.objects.create(
                doctor=doctor,
                message=f"New treatment added for patient {treatment.patient.name}."
            )

            return redirect(
                "doctor_dashboard"
            )

    else:

        form = TreatmentForm()

    return render(
        request,
        "add_treatment.html",
        {
            "form": form,
            "doctor": doctor,
        }
    )


# =========================================================
# VIEW PATIENT RECORD
# =========================================================
def view_patient_record(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    assignment = PatientDoctorAssignment.objects.filter(
        patient_id=patient_id
    ).first()

    return render(
        request,
        "patient_record.html",
        {
            "patient": patient,
            "assignment": assignment,
        }
    )


# =========================================================
# TREATMENT HISTORY - DOCTOR
# =========================================================
def treatment_history(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    treatments = Treatment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient"
    ).order_by(
        "-treatment_date"
    )

    return render(
        request,
        "treatment_history.html",
        {
            "doctor": doctor,
            "treatments": treatments,
        }
    )


# =========================================================
# DOCTOR APPOINTMENTS
# =========================================================
def doctor_appointments(request):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient"
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    return render(
        request,
        "doctor_appointments.html",
        {
            "doctor": doctor,
            "appointments": appointments,
        }
    )


# =========================================================
# UPDATE APPOINTMENT STATUS
# =========================================================
def update_appointment_status(request, id):

    doctor = Doctor.objects.filter(
        username=request.session.get(
            "doctor_username"
        )
    ).first()

    if not doctor:

        return redirect(
            "login"
        )

    appointment = get_object_or_404(
        Appointment,
        id=id,
        doctor=doctor
    )

    if request.method == "POST":

        status = request.POST.get(
            "status"
        )

        if status in [
            "SCHEDULED",
            "COMPLETED",
            "CANCELLED"
        ]:

            appointment.status = status

            appointment.save()

        return redirect(
            "doctor_appointments"
        )

    return redirect(
        "doctor_appointments"
    )


# =========================================================
# DELETE TREATMENT
# =========================================================
def delete_treatment(request, id):

    treatment = get_object_or_404(
        Treatment,
        id=id
    )

    treatment.delete()

    return redirect(
        "treatment_history"
    )


# =========================================================
# EDIT TREATMENT
# =========================================================
def edit_treatment(request, id):

    treatment = get_object_or_404(
        Treatment,
        id=id
    )

    if request.method == "POST":

        old_status = treatment.status

        treatment.patient_id = request.POST.get(
            "patient"
        )

        treatment.treatment_name = request.POST.get(
            "treatment_name"
        )

        treatment.description = request.POST.get(
            "description"
        )

        treatment.treatment_date = request.POST.get(
            "treatment_date"
        )

        treatment.status = request.POST.get(
            "status"
        )

        treatment.save()

        # =================================================
        # TREATMENT COMPLETED NOTIFICATION
        # =================================================

        if (
            old_status != "COMPLETED"
            and treatment.status == "COMPLETED"
        ):

            Notification.objects.create(
                doctor=treatment.doctor,
                message=f"Treatment {treatment.treatment_name} for patient {treatment.patient.name} has been completed."
            )

        # =================================================
        # TREATMENT UPDATED NOTIFICATION
        # =================================================

        else:

            Notification.objects.create(
                doctor=treatment.doctor,
                message=f"Treatment for patient {treatment.patient.name} has been updated."
            )

        return redirect(
            "treatment_history"
        )

    return render(
        request,
        "edit_treatment.html",
        {
            "treatment": treatment
        }
    )

# =========================
# ADD MEDICAL RECORD - DOCTOR
# =========================
def add_medical_record(request):

    doctor = Doctor.objects.filter(
        username=request.session.get("doctor_username")
    ).first()

    if not doctor:
        return redirect("login")

    if request.method == "POST":

        form = MedicalRecordForm(request.POST)

        if form.is_valid():

            medical_record = form.save(
                commit=False
            )

            # Automatically assign logged-in doctor
            medical_record.doctor = doctor

            medical_record.save()

            return redirect(
                "patient_records"
            )

    else:

        form = MedicalRecordForm()

    # Show only patients assigned to this doctor
    assigned_patient_ids = PatientDoctorAssignment.objects.filter(
        doctor=doctor
    ).values_list(
        "patient_id",
        flat=True
    )

    form.fields["patient"].queryset = Patient.objects.filter(
        id__in=assigned_patient_ids
    )

    return render(
        request,
        "add_medical_record.html",
        {
            "form": form,
            "doctor": doctor,
        }
    )

