from django.contrib import admin
from .models import Doctor, User, UserType, Patient, Appointment
from .forms import DoctorForm, PatientForm


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorForm


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm

    list_display = (
        "name",
        "email",
        "phone",
        "gender",
        "blood_group",
        "username",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "username",
    )

    list_filter = (
        "gender",
        "blood_group",
    )


admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Appointment)