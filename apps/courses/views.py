from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course, Enrollment, CourseProgress
from .forms import CourseForm

from django.core.paginator import Paginator
from django.db.models import Q

# import the necessary  module and liberary for pdf generations 
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# from .models import Course, Enrollment, CourseProgress
# from .forms import CourseForm

# from django.core.paginator import Paginator
# from django.db.models import Q


@login_required
def course_list(request):

    query = request.GET.get("q", "")
    level = request.GET.get("level", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "")

    # Get all courses first
    courses = Course.objects.all()

    # Search
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by level
    if level:
        courses = courses.filter(level=level)

    # Filter by status
    if status:
        courses = courses.filter(status=status)

    # Sorting
    if sort == "oldest":
        courses = courses.order_by("created_at")

    elif sort == "title":
        courses = courses.order_by("title")

    elif sort == "price_low":
        courses = courses.order_by("price")

    elif sort == "price_high":
        courses = courses.order_by("-price")

    else:
        courses = courses.order_by("-created_at")

    # Pagination (AFTER filtering and sorting)
    paginator = Paginator(courses, 6)

    page_number = request.GET.get("page")

    courses = paginator.get_page(page_number)
    # Recent courses
    recent_courses = Course.objects.order_by("-created_at")[:5]
    

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
            "query": query,
            "level": level,
            "status": status,
            "sort": sort,
            
            "total_courses": Course.objects.count(),
            "published_courses": Course.objects.filter(status="published").count(),
            "draft_courses": Course.objects.filter(status="draft").count(),
            
            "beginner_courses": Course.objects.filter(level="beginner").count(),
            "intermediate_courses": Course.objects.filter(level="intermediate").count(),
            "advanced_courses": Course.objects.filter(level="advanced").count(),
            
            "recent_courses": recent_courses,
        }
    )
 

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    is_enrolled = False

    if request.user.role == "student":
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

    progress = None

    if is_enrolled:
        enrollment = Enrollment.objects.get(
            student=request.user,
            course=course
        )

        progress, created = CourseProgress.objects.get_or_create(
    student=request.user,
    course=course,
)

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "is_enrolled": is_enrolled,
            "progress": progress,
        }
    )
    

@login_required
def enroll_course(request, pk):

    course = get_object_or_404(Course, pk=pk)

    # Only students can enroll
    if request.user.role != "student":
        messages.error(
            request,
            "Only students can enroll in courses."
        )
        return redirect("courses:course_detail", pk=course.pk)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        messages.success(
            request,
            "Successfully enrolled in the course!"
        )
    else:
        messages.info(
            request,
            "You are already enrolled."
        )

    return redirect("courses:course_detail", pk=course.pk)

@login_required
def update_progress(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.user.role != "student":
        messages.error(
            request,
            "Only students can update progress."
        )
        return redirect("courses:course_detail", pk=course.pk)

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course
    )

    progress, created = CourseProgress.objects.get_or_create(
        enrollment=enrollment
    )

    if request.method == "POST":

        percent = int(request.POST.get("progress", 0))

        if percent < 0:
            percent = 0

        if percent > 100:
            percent = 100

        progress.progress = percent

        if percent == 100:
            progress.completed = True
            enrollment.status = "completed"
            enrollment.save()

        progress.save()

        messages.success(
            request,
            "Progress updated successfully."
        )

    return redirect(
        "courses:course_detail",
        pk=course.pk
    )

@login_required
def course_certificate(request, pk):

    course = get_object_or_404(Course, pk=pk)

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course,
    )

    progress = get_object_or_404(
        CourseProgress,
        student=request.user,
        course=course,
    )

    if progress.progress < 100:
        messages.error(
            request,
            "Complete the course to access your certificate."
        )
        return redirect("courses:course_detail", pk=course.pk)

    return render(
        request,
        "courses/course_certificate.html",
        {
            "course": course,
            "progress": progress,
            "enrollment": enrollment,
        }
    )
    
# for couce certificate generations and download as pdf file 

@login_required
def download_certificate(request, pk):

    course = get_object_or_404(Course, pk=pk)

    progress = get_object_or_404(
        CourseProgress,
        student=request.user,
        course=course,
    )

    if progress.progress < 100:
        messages.error(
            request,
            "Complete the course first."
        )
        return redirect("courses:course_detail", pk=pk)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    normal = styles["BodyText"]
    normal.alignment = TA_CENTER

    story = []

    story.append(Paragraph("Certificate of Completion", title))
    story.append(Paragraph("<br/><br/>", normal))
    story.append(
        Paragraph(
            f"This certifies that <b>{request.user.get_full_name() or request.user.username}</b>",
            heading,
        )
    )

    story.append(Paragraph("<br/>has successfully completed<br/><br/>", normal))

    story.append(
        Paragraph(
            f"<b>{course.title}</b>",
            heading,
        )
    )

    story.append(Paragraph("<br/><br/>Congratulations!", normal))

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{course.title}_certificate.pdf"'
    )

    return response
 
    
@login_required
def my_courses(request):

    if request.user.role != "student":
        messages.error(
            request,
            "Only students can access this page."
        )
        return redirect("courses:course_list")

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    progress_records = CourseProgress.objects.filter(
        student=request.user
    )

    progress_map = {
        progress.course_id: progress
        for progress in progress_records
    }

    total_courses = enrollments.count()

    completed_courses = progress_records.filter(
        progress=100
    ).count()

    if total_courses > 0:

        average_progress = sum(
            p.progress for p in progress_records
        ) / total_courses

    else:

        average_progress = 0

    return render(
        request,
        "courses/my_courses.html",
        {
            "enrollments": enrollments,
            "progress_map": progress_map,
            "total_courses": total_courses,
            "completed_courses": completed_courses,
            "average_progress": round(average_progress, 1),
        }
    )
    
    

@login_required
def course_create(request):

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.created_by = request.user
            course.save()
         
            messages.success(
                request,
                "Course created successfully."
            )

            return redirect("courses:course_list")

    else:
        form = CourseForm()

    return render(
        request,
        "courses/course_create.html",
        {
            "form": form
        }
    )


@login_required
def course_update(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.user != course.teacher and not request.user.is_superuser:
        messages.error(request, "You are not allowed to edit this course.")
        return redirect("courses:course_detail", pk=course.pk)

    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect(
                "courses:course_detail",
                pk=course.pk
            )

    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "courses/course_update.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
def course_delete(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.user != course.teacher and not request.user.is_superuser:
        messages.error(request, "You are not allowed to delete this course.")
        return redirect("courses:course_detail", pk=course.pk)

    if request.method == "POST":
        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect("courses:course_list")

    return render(
        request,
        "courses/course_delete.html",
        {
            "course": course
        }
    )