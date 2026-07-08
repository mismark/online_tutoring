from django.shortcuts import render, get_object_or_404

from .models import Certificate

from django.contrib.auth.decorators import login_required

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
    

def certificate_list(request):
    certificates= Certificate.objects.filter(
        student = request.user
    ).order_by(
        "-issued_at"
    )
    
    return render(
        request,
        "certificates/certificate_list.html",
        {
            "certificates":certificates
        }
    )