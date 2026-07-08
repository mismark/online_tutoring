from django.shortcuts import render, get_object_or_404
from .models import Certificate


def verify_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate,
        certificate_id=certificate_id
    )

    context = {
        "certificate": certificate,
    }

    return render(
        request,
        "certificates/verify_certificate.html",
        context
    )