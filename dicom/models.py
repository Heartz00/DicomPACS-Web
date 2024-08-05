# dicom/models.py

from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Study(models.Model):
    study_id = models.CharField(max_length=100, unique=True)
    patient_name = models.CharField(max_length=255, db_index=True)
    patient_id = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    study_date = models.DateField(null=True)
    study_description = models.CharField(max_length=255, blank=True, null=True)
    modality = models.CharField(max_length=50, null=True, blank=True)
    body_part = models.CharField(max_length=100, null=True, blank=True)
    procedure = models.CharField(max_length=255, null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.study_description}"

class DICOMImage(models.Model):
    file = models.FileField(upload_to='dicom_images/')
    patient_id = models.CharField(max_length=50)
    patient_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    modality = models.CharField(max_length=50)
    body_part = models.CharField(max_length=100)
    study = models.ForeignKey(Study, related_name='images', on_delete=models.CASCADE)
    accession_number = models.CharField(max_length=100, null=True, blank=True)
    number_of_series = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    additional_documents = models.FileField(upload_to='additional_docs/', null=True, blank=True)
    dicom_url = models.URLField(max_length=200, null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.patient_name} - {self.modality}"

class AdditionalDocument(models.Model):
    file = models.FileField(upload_to='additional_documents/')
    study = models.ForeignKey(Study, related_name='additional_documents', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Document for {self.study.patient_name}"
