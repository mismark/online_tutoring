from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    user = request.user

    if user.role == "admin":
        template = "dashboard/admin_dashboard.html"

    elif user.role == "teacher":
        template = "dashboard/teacher_dashboard.html"

    elif user.role == "student":
        template = "dashboard/student_dashboard.html"

    elif user.role == "parent":
        template = "dashboard/parent_dashboard.html"

    else:
        template = "dashboard/home.html"

    return render(
        request,
        template,
        {
            "user": user
        }
    )