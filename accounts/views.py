from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse

from .models import User, PatientProfile, EmergencyContact
from .forms import (
    PatientRegistrationForm,
    DoctorRegistrationForm,
    LoginForm,
    PatientProfileForm,
    EmergencyContactForm
)
from .forms import PatientRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

def patient_register(request):

    if request.method == "POST":

        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            return render(
                request,
                "accounts/registration_success.html",
                {"user": user}
            )

    else:
        form = PatientRegistrationForm()

    return render(
        request,
        "accounts/patient_register.html",
        {"form": form}
    )

def doctor_register(request):

    if request.method == "POST":

        form = DoctorRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            return render(
                request,
                "accounts/doctor_registration_success.html",
                {"user": user}
            )

    else:
        form = DoctorRegistrationForm()

    return render(
        request,
        "accounts/doctor_register.html",
        {"form": form}
    )


def doctor_login(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                email=email,
                password=password
            )

            if user is not None:

                if user.role == "DOCTOR":
                    login(request, user)

                    return redirect("doctor_dashboard")

                else:
                    form.add_error(
                        None,
                        "This login is only for doctors."
                    )

            else:
                form.add_error(
                    None,
                    "Invalid email or password."
                )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/doctor_login.html",
        {"form": form}
    )
@login_required
def doctor_dashboard(request):

    if request.user.role != "DOCTOR":
        return redirect("patient_dashboard")

    if request.user.verification_status != "VERIFIED":
        return render(
            request,
            "accounts/doctor_not_verified.html"
        )

    return render(
        request,
        "accounts/doctor_dashboard.html"
    )


def patient_login(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                email=email,
                password=password
            )

            if user is not None:

                if user.role == "PATIENT":
                    login(request, user)

                    return redirect("patient_dashboard")

                else:
                    form.add_error(
                        None,
                        "This login is only for patients."
                    )

            else:
                form.add_error(
                    None,
                    "Invalid email or password."
                )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/patient_login.html",
        {"form": form}
    )
@login_required
def patient_dashboard(request):

    return render(
        request,
        "accounts/patient_dashboard.html"
    )
@login_required
def patient_profile(request):

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = PatientProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect("patient_profile")

    else:
        form = PatientProfileForm(
            instance=profile
        )

    return render(
        request,
        "accounts/patient_profile.html",
        {"form": form}
    )
@login_required
def patient_dashboard(request):

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = PatientProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("patient_dashboard")

    else:
        form = PatientProfileForm(
            instance=profile
        )

    return render(
        request,
        "accounts/patient_dashboard.html",
        {"form": form}
    )
@login_required
def emergency_contact(request):

    contact, created = EmergencyContact.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = EmergencyContactForm(
            request.POST,
            instance=contact
        )

        if form.is_valid():
            form.save()

            return redirect("emergency_contact")

    else:
        form = EmergencyContactForm(
            instance=contact
        )

    return render(
        request,
        "accounts/emergency_contact.html",
        {"form": form}
    )
@login_required
def lifevault_card(request):

    user = request.user

    if not user.qr_code:

        emergency_url = (
            f"http://192.168.1.111:8000"
            f"{reverse('emergency_access', args=[user.lifevault_id])}"
        )

        qr = qrcode.make(emergency_url)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        user.qr_code.save(
            f"{user.lifevault_id}.png",
            ContentFile(buffer.getvalue()),
            save=True
        )

    return render(
        request,
        "accounts/lifevault_card.html",
        {"user": user}
    )
def emergency_access(request, lifevault_id):

    user = User.objects.filter(
        lifevault_id=lifevault_id,
        role="PATIENT"
    ).first()

    if not user:
        return render(
            request,
            "accounts/emergency_access.html",
            {"error": "Patient not found"}
        )

    return render(
        request,
        "accounts/emergency_access.html",
        {"patient": user}
    )