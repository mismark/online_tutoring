from django.shortcuts import render, get_object_or_404

from .models import Certificate



def verify_certificate(request, certificate_id):


    try:

        certificate = Certificate.objects.get(
            certificate_id=certificate_id
        )


    except Certificate.DoesNotExist:

        certificate = None



    return render(
        request,
        "certificates/verify_certificate.html",
        {
            "certificate": certificate
        }
    )