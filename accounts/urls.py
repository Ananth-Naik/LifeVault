from django.urls import path
from . import views


urlpatterns = [
    path(
        "register/",
        views.patient_register,
        name="patient_register"
    ),

    path(
        "login/",
        views.patient_login,
        name="patient_login"
    ),

    path(
        "dashboard/",
        views.patient_dashboard,
        name="patient_dashboard"
    ),
    path(
    "profile/",
    views.patient_profile,
    name="patient_profile"
),
path(
    "emergency-contact/",
    views.emergency_contact,
    name="emergency_contact"
),
path("lifevault-card/", views.lifevault_card, name="lifevault_card"),


path(
    "emergency/<str:lifevault_id>/",
    views.emergency_access,
    name="emergency_access"
),
path(
    "doctor-register/",
    views.doctor_register,
    name="doctor_register"
),
path(
    "doctor-login/",
    views.doctor_login,
    name="doctor_login"
),

path(
    "doctor-dashboard/",
    views.doctor_dashboard,
    name="doctor_dashboard"
),


]

