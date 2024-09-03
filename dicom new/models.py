from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    patient_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=10, null=True, blank=True)
    study_description = models.CharField(max_length=255, null=True, blank=True)
    study_date = models.CharField(max_length=10)
    modalities_in_study = models.CharField(max_length=64, null=True, blank=True)
    accession_number = models.CharField(max_length=64, null=True, blank=True)
    number_of_series = models.IntegerField(default=0)

    def __str__(self):
        return self.name


