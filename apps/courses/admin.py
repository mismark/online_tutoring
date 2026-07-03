from django.contrib import admin
from .models import Course


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
        "teacher__username",
    )

    ordering = (
        "-created_at",
    )