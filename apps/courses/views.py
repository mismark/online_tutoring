from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course
from .forms import CourseForm

from django.core.paginator import Paginator
from django.db.models import Q

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
        }
    )


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course
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