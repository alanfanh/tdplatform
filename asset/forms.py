from django import forms

from .models import Complaint, TecContent, Patent

class TecContentForm(forms.ModelForm):
    class Meta:
        model = TecContent
        fields = ("tname","group","author","body","file","award")

class ComplaintForm(forms.ModelForm):
    ctime = forms.DateTimeField(
        input_formats=['%Y-%m-%d'], widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    class Meta:
        model = Complaint
        fields = ("cname","type","submitter","oa_number","asset_number","ctime", "area", "product", "product_line", "version", "level", "product_line", "category", "tester", "analysis_status", "analysis_time", "status", "complete_time","solutions", "closed_time", "cfile", "description")

class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ("name","type","author","group","submit_time", "status", "patent_id", "award", "file")