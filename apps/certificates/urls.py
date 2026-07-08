from django.urls import path
from . import views


app_name = "certificates"


urlpatterns = [

    path(
        "verify/<uuid:certificate_id>/",
        views.verify_certificate,
        name="verify_certificate"
    ),
    
    path(
        "my-certificates/",
        views.certificate_list,
        name = "certificate_list"
    ),

]