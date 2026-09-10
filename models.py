from django.db import models


# =========================
# USER TYPE MODEL
# =========================
class UserType(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name


# =========================
# USER MODEL
# =========================
class User(models.Model):

    username = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    user_type = models.CharField(
        max_length=10,
        choices=[
            ("ADMIN", "Admin"),
            ("DOCTOR", "Doctor"),
            ("PATIENT", "Patient"),
        ]
    )

    def __str__(self):
        return self.username


# =========================
# DOCTOR MODEL
# =========================
class Doctor(models.Model):

    user_type = models.ForeignKey(
        UserType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    specialization = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    username = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    password = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.user_type:
            self.user_type = UserType.objects.get(
                name="doctor"
            )

        super().save(*args, **kwargs)

        User.objects.update_or_create(
            username=self.username,
            defaults={
                "email": self.email,
                "password": self.password,
                "user_type": "DOCTOR"
            }
        )

    def __str__(self):
        return self.name


# =========================
# PATIENT MODEL
# =========================
class Patient(models.Model):

    user_type = models.ForeignKey(
        UserType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20
    )

    blood_group = models.CharField(
        max_length=10
    )

    address = models.TextField()

    emergency_contact = models.CharField(
        max_length=15
    )

    username = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    password = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.user_type:
            self.user_type = UserType.objects.get(
                name="patient"
            )

        old_user = None

        if self.pk:
            try:
                old_patient = Patient.objects.get(
                    pk=self.pk
                )

                if old_patient.username:

                    old_user = User.objects.filter(
                        username=old_patient.username,
                        user_type="PATIENT"
                    ).first()

            except Patient.DoesNotExist:
                pass

        if not self.password and old_user:
            self.password = old_user.password

        super().save(*args, **kwargs)

        User.objects.update_or_create(
            username=self.username,
            defaults={
                "email": self.email,
                "password": self.password,
                "user_type": "PATIENT"
            }
        )

    def __str__(self):
        return self.name


# =========================
# PATIENT DOCTOR ASSIGNMENT
# =========================
class PatientDoctorAssignment(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="assigned_patients"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="assigned_doctors"
    )

    assigned_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.doctor.name} - {self.patient.name}"


# =========================
# TREATMENT MODEL
# =========================
class Treatment(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="treatments"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="treatments"
    )

    treatment_name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    treatment_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("COMPLETED", "Completed"),
        ],
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.name} - {self.treatment_name}"


# =========================
# APPOINTMENT MODEL
# =========================
class Appointment(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    appointment_type = models.CharField(
        max_length=30,
        choices=[
            ("FOLLOW_UP", "Follow-up"),
            ("CHEMOTHERAPY", "Chemotherapy"),
            ("RADIATION", "Radiation Therapy"),
            ("REVIEW", "Review"),
        ],
        default="FOLLOW_UP"
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("SCHEDULED", "Scheduled"),
            ("COMPLETED", "Completed"),
            ("CANCELLED", "Cancelled"),
        ],
        default="SCHEDULED"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient.name} - "
            f"{self.doctor.name} - "
            f"{self.appointment_date}"
        )


# =========================
# MEDICAL RECORD MODEL
# =========================
class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )

    record_title = models.CharField(
        max_length=200
    )

    record_type = models.CharField(
        max_length=100,
        choices=[
            ("BLOOD_TEST", "Blood Test"),
            ("CT_SCAN", "CT Scan"),
            ("MRI_SCAN", "MRI Scan"),
            ("BIOPSY", "Biopsy"),
            ("X_RAY", "X-Ray"),
            ("DIAGNOSIS", "Diagnosis Report"),
            ("OTHER", "Other"),
        ]
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    record_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient.name} - "
            f"{self.record_title}"
        )


# =========================
# NOTIFICATION MODEL
# =========================
class Notification(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.doctor.name} - {self.message}"

