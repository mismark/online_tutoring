from django.shortcuts import render, get_object_or_404

from .models import Certificate


def verify_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate,
        certificate_id=certificate_id
    )
    
    certificate = Certificate.objects.get(
    student=request.user,
    course=course,
  )

    return render(

    request,

    "courses/certificate.html",

    {

        "course":course,

        "progress":progress,

        "certificate":certificate,

        "qr_code":qr_code,

    }

)