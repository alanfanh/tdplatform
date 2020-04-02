from django import forms

from .models import Complaint, TecContent

class TecContentForm(forms.ModelForm):
    class Meta:
        model = TecContent
        fields = ("tname","group","author","body","file")

class ComplaintForm(forms.ModelForm):
    ctime = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    complete_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Complaint
        fields = ("cname","type","submitter","ctime","product","version", "level", "product_line", "category", "tester", "complete_time", "status", "cfile")
