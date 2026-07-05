from django.contrib import admin

from .models import Course, Enrollment, CourseProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "teacher",
        "price",
        "level",
        "status",
        "created_at",
    )

    list_filter = (
        "level",
        "status",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "status",
        "enrolled_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "student__username",
        "course__title",
    )
    
@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "progress",
        "last_accessed",
    )

    list_filter = (
        "progress",
    )

    search_fields = (
        "student__username",
        "course__title",
    )    