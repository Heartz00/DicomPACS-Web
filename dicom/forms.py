# dicom/forms.py

from django import forms
from .models import Study, DICOMImage, AdditionalDocument
from userauths.models import Doctor
from multiupload.fields import MultiFileField




class DICOMUploadForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=500, max_file_size=1024*1024*50, required=False)  # File upload field
    folder = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': False, 'webkitdirectory': True, 'directory': True, 'accept': 'application/dicom'}))  # Folder upload field

    def clean(self):
        cleaned_data = super().clean()
        files = cleaned_data.get('files')
        folder = cleaned_data.get('folder')

        if not files and not folder:
            raise forms.ValidationError("Either files or folder must be provided.")

        # Validate folder upload if present
        if folder:
            # Handle folder upload logic here, if needed
            pass

        return cleaned_data
    

class StudyDetailForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            'patient_name', 'patient_id', 'birth_date', 'gender', 'phone_number',
            'modality', 'body_part', 'procedure', 'study_description', 'study_date', 
            'medical_history'
        ]

class ReportForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['report']

class AdditionalDocumentForm(forms.ModelForm):
    class Meta:
        model = AdditionalDocument
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError("No file uploaded.")
        return file

class AssignStudyForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=True, label='Assign to Doctor')
