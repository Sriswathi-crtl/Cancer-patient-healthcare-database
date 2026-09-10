from django import forms
from .models import (
    Doctor,
    Patient,
    PatientDoctorAssignment,
    Treatment,
    Appointment,
    MedicalRecord
)

import re


# =========================
# DOCTOR FORM
# =========================
class DoctorForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=False
    )

    class Meta:
        model = Doctor

        fields = [
            "name",
            "email",
            "phone",
            "specialization",
            "department",
            "username",
            "password",
            "confirm_password",
        ]

        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise forms.ValidationError(
                "Name is required."
            )

        if not re.match(r"^[A-Za-z\s.]+$", name):
            raise forms.ValidationError(
                "Invalid name. Name should contain only letters."
            )

        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError(
                "Email is required."
            )

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        if not phone.isdigit():
            raise forms.ValidationError(
                "Invalid phone number. Enter numbers only."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Invalid phone number. Enter a 10-digit phone number."
            )

        return phone

    def clean_specialization(self):
        specialization = self.cleaned_data.get("specialization")

        if not specialization:
            raise forms.ValidationError(
                "Specialization is required."
            )

        if not re.match(r"^[A-Za-z\s]+$", specialization):
            raise forms.ValidationError(
                "Invalid specialization. Enter letters only."
            )

        return specialization

    def clean_department(self):
        department = self.cleaned_data.get("department")

        if not department:
            raise forms.ValidationError(
                "Department is required."
            )

        if not re.match(r"^[A-Za-z\s]+$", department):
            raise forms.ValidationError(
                "Invalid department. Enter letters only."
            )

        return department

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError(
                "Username is required."
            )

        existing_doctor = Doctor.objects.filter(
            username=username
        ).first()

        if existing_doctor and existing_doctor.pk != self.instance.pk:
            raise forms.ValidationError(
                "Username already exists. Please choose another username."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password:

            if not confirm_password:
                raise forms.ValidationError(
                    "Please enter Confirm Password."
                )

            if password != confirm_password:
                raise forms.ValidationError(
                    "Password and Confirm Password do not match."
                )

        return cleaned_data


# =========================
# PATIENT FORM
# =========================
class PatientForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1940, 2027)
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=False
    )

    class Meta:
        model = Patient

        fields = [
            "name",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "blood_group",
            "address",
            "emergency_contact",
            "username",
            "password",
            "confirm_password",
        ]

        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Leave blank to keep current password"
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise forms.ValidationError(
                "Name is required."
            )

        if not re.match(r"^[A-Za-z\s.]+$", name):
            raise forms.ValidationError(
                "Invalid name. Name should contain only letters."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        if not phone.isdigit():
            raise forms.ValidationError(
                "Invalid phone number. Enter numbers only."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Invalid phone number. Enter a 10-digit phone number."
            )

        return phone

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError(
                "Username is required."
            )

        existing_patient = Patient.objects.filter(
            username=username
        ).first()

        if existing_patient and existing_patient.pk != self.instance.pk:
            raise forms.ValidationError(
                "Username already exists. Please choose another username."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not self.instance.pk and not password:

            self.add_error(
                "password",
                "Password is required for a new patient."
            )

        if password:

            if not confirm_password:

                self.add_error(
                    "confirm_password",
                    "Please confirm your new password."
                )

            elif password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "Password and Confirm Password do not match."
                )

        return cleaned_data


# =========================
# PATIENT DOCTOR ASSIGNMENT FORM
# =========================
class PatientDoctorAssignmentForm(forms.ModelForm):

    class Meta:
        model = PatientDoctorAssignment

        fields = [
            "doctor",
            "patient"
        ]


# =========================
# TREATMENT FORM
# =========================
class TreatmentForm(forms.ModelForm):

    class Meta:
        model = Treatment

        fields = [
            "patient",
            "treatment_name",
            "description",
            "treatment_date",
            "status",
        ]

        widgets = {

            "treatment_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter treatment name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter treatment description",
                    "rows": 5
                }
            ),

            "treatment_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "status": forms.Select(),
        }


# =========================
# APPOINTMENT FORM
# =========================
class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            "doctor",
            "appointment_date",
            "appointment_time",
            "appointment_type",
            "reason",
        ]

        widgets = {

            "doctor": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "appointment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "appointment_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time"
                }
            ),

            "appointment_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter appointment reason",
                    "rows": 4
                }
            ),
        }


# =========================
# MEDICAL RECORD FORM
# =========================
class MedicalRecordForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord

        fields = [
            "patient",
            "record_title",
            "record_type",
            "description",
            "record_date",
        ]

        widgets = {

            "patient": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "record_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter medical record title"
                }
            ),

            "record_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter medical record description",
                    "rows": 4
                }
            ),

            "record_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }
