from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    
    def clean_price(self):

        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Price cannot be negative."
            )

        return price

    class Meta:
        model = Course

        fields = [
            "title",
            "description",
            "thumbnail",
            "price",
            "level",
            "status",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Course Title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Course Description"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Course Price"
                }
            ),

            "level": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "thumbnail": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }