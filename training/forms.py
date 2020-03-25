from django import forms
from .models import Course

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("cname","range","course_time","address","teacher","cdescription","file_name","student")