import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render

from .services import send_contact_email

NAME_MAX = 100
EMAIL_MAX = 254
SUBJECT_MAX = 200
MESSAGE_MAX = 5000
GENERIC_SEND_ERROR = "Your message could not be sent. Please try again later."


def _single_line(value):
    if value is None:
        return ""
    return re.sub(r"[\r\n]+", " ", str(value)).strip()


def contact(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    name = _single_line(request.POST.get("name"))
    email = _single_line(request.POST.get("email"))
    subject = _single_line(request.POST.get("subject"))
    message = (request.POST.get("message") or "").replace("\r\n", "\n").replace("\r", "\n").strip()

    if not name or not email or not subject or not message:
        return JsonResponse(
            {"status": "error", "message": "Please complete all required fields."},
            status=400,
        )

    if (
        len(name) > NAME_MAX
        or len(email) > EMAIL_MAX
        or len(subject) > SUBJECT_MAX
        or len(message) > MESSAGE_MAX
    ):
        return JsonResponse(
            {"status": "error", "message": "One of the fields is too long."},
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"status": "error", "message": "Please enter a valid email address."},
            status=400,
        )

    try:
        send_contact_email(name, email, subject, message)
    except Exception:
        return JsonResponse({"status": "error", "message": GENERIC_SEND_ERROR}, status=500)

    return JsonResponse({"status": "success", "message": "Message sent!"})


def index(request):
    context = {}
    return render(request, "index.html", context)
