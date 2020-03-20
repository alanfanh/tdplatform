from django import forms

from .models import Complaint, TecContent

class TecContentForm(forms.ModelForm):
    class Meta:
        model = TecContent
        fields = ("tname","tag","author","body","created_at","file")


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ("cname","type","submitter","ctime","product","version", "level", "product_line", "category", "tester", "complete_time", "status", "cfile")
