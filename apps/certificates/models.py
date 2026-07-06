import uuid

from django.db import models
from django.conf import settings

from apps.courses.models import Course


class Certificate(models.Model):

    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "student",
            "course",
        )

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"