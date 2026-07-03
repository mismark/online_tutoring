from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "teacher",
        "price",
        "level",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "level",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "teacher__username",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Course Information",
            {
                "fields": (
                    "title",
                    "description",
                    "thumbnail",
                    "teacher",
                )
            },
        ),
        (
            "Course Settings",
            {
                "fields": (
                    "price",
                    "level",
                    "status",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )