from django import forms

from .models import Complaint, TecContent, Patent, Project

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

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name","type","created_at","completed_time","coder","developer","tester","newbug_percent","reopen_count","missing_percent", "nocase_found","test_round", "reject_count", "reject_reason", "deliver", "delay", "delay_percent", "delay_reason", "day_round", "per_version", "perf_count", "beta_bug","customer_bug", "quality_issue","solution","cost_percent","pcb_count","item_percent","tec_count", "tec","note")