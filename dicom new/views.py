from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Patient
import requests
import os

ORTHANC_BASE_URL = os.getenv('ORTHANC_BASE_URL')
OHIF_VIEWER_URL = os.getenv('OHIF_VIEWER_URL')

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_detail.html', {'patient': patient})
def upload_dicom(request):
    if request.method == 'POST':
        dicom_file = request.FILES['dicom_file']
        files = {'file': dicom_file}
        try:
            response = requests.post(f'{ORTHANC_BASE_URL}/instances', files=files)
            response.raise_for_status()  # Check for HTTP errors

            print('Response Status Code:', response.status_code)
            print('Response Content:', response.text)

            if response.status_code == 200:
                response_json = response.json()
                instance_id = response_json.get('ID')
                
                instance_metadata_response = requests.get(f'{ORTHANC_BASE_URL}/instances/{instance_id}/tags')
                instance_metadata_response.raise_for_status()

                metadata = instance_metadata_response.json()

                print('Metadata:', metadata)

                Patient.objects.create(
                    patient_id=metadata.get('0010,0020', ''),
                    name=metadata.get('0010,0010', ''),
                    birth_date=metadata.get('0010,0030', ''),
                    study_description=metadata.get('0008,1030', ''),
                    study_date=metadata.get('0008,0020', ''),
                    modalities_in_study=metadata.get('0008,0061', ''),
                    accession_number=metadata.get('0008,0050', ''),
                    number_of_series=metadata.get('0020,1206', 0)
                )

                return HttpResponseRedirect(reverse('patient_list'))
        except requests.RequestException as e:
            print(f'Request failed: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')
    
    return render(request, 'upload.html')

