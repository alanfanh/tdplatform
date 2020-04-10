from django import forms

from .models import Complaint, TecContent

class TecContentForm(forms.ModelForm):
    class Meta:
        model = TecContent
        fields = ("tname","group","author","body","file")

class ComplaintForm(forms.ModelForm):
    ctime = forms.DateTimeField(
        input_formats=['%Y-%m-%d'], widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    complete_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d'], widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    class Meta:
        model = Complaint
        fields = ("cname","type","submitter","oa_number","ctime","area","product", "product_line","version", "level", "product_line", "category", "tester", "complete_time", "status", "cfile", "description")
