from django import forms

class BrdUploadForm(forms.Form):
    brd_file = forms.FileField(label="Upload BRD PDF", help_text="Select your Business Requirement Document (PDF format)")