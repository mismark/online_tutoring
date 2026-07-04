from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course
from .forms import CourseForm


from django.db.models import Q

@login_required
def course_list(request):

    query = request.GET.get("q")
    level = request.GET.get("level")
    status = request.GET.get("status")
    sort = request.GET.get("sort")

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if level:
        courses = courses.filter(level=level)

    if status:
        courses = courses.filter(status=status)

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

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
            "query": query,
            "level": level,
            "status": status,
            "sort": sort,
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