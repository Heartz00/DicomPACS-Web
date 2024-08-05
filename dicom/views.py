# dicom/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.uploadedfile import TemporaryUploadedFile  # Add this import
from .forms import DICOMUploadForm, StudyDetailForm, ReportForm, AdditionalDocumentForm, AssignStudyForm
from .models import DICOMImage, Study, Institution
from userauths.models import Doctor  # Assuming you have a Doctor model in userauths app
import pydicom
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
import numpy as np
import logging
import matplotlib.pyplot as plt
from pydicom.pixel_data_handlers.util import convert_color_space
import SimpleITK as sitk
import os 
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages



logger = logging.getLogger(__name__)


def upload_view(request):
    if request.method == 'POST':
        form = DICOMUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle folder upload
            folder = request.FILES.get('folder')
            if folder:
                for uploaded_file in folder:
                    try:
                        if isinstance(uploaded_file, TemporaryUploadedFile):
                            uploaded_file_name = uploaded_file.name
                        else:
                            uploaded_file_name = os.path.basename(uploaded_file.name)

                        process_dicom_file(uploaded_file.read(), uploaded_file_name)  # Pass bytes instead of file object

                    except Exception as e:
                        if 'uploaded_file_name' not in locals():  # Check if uploaded_file_name is defined
                            uploaded_file_name = None  # Assign a default value if not defined
                        messages.error(request, f"Error processing file {uploaded_file_name}: {str(e)}")
                messages.success(request, f"DICOM files from folder uploaded successfully.")
                return redirect('dicom:dicom_list')
            
            # Handle individual files upload
            files = request.FILES.getlist('files')
            if files:
                for uploaded_file in files:
                    try:
                        process_dicom_file(uploaded_file.read(), uploaded_file.name)  # Pass bytes instead of file object
                    except Exception as e:
                        messages.error(request, f"Error processing file {uploaded_file.name}: {str(e)}")
                messages.success(request, f"{len(files)} DICOM files uploaded successfully.")
                return redirect('dicom:dicom_list')
    else:
        form = DICOMUploadForm()

    return render(request, 'dicom/upload.html', {'form': form})

def process_dicom_file(uploaded_file, uploaded_file_name):
    # Example function to process a DICOM file
    if isinstance(uploaded_file, bytes):
        uploaded_file = io.BytesIO(uploaded_file)  # Convert bytes to a file-like object

    ds = pydicom.dcmread(uploaded_file)

    # Extract metadata
    patient_id = ds.get('PatientID', 'Unknown')
    patient_name = ds.get('PatientName', 'Unknown')
    if patient_name != 'Unknown':
        patient_name = str(patient_name).replace('^', ' ')

    birth_date_str = ds.get('PatientBirthDate', None)
    birth_date = datetime.strptime(birth_date_str, '%Y%m%d').date() if birth_date_str else None

    gender = ds.get('PatientSex', 'Unknown')
    body_part = ds.get('BodyPartExamined', 'Unknown')
    modality = ds.get('Modality', 'Unknown')
    study_description = ds.get('StudyDescription', 'No Description')  # Add this line
    study_id = ds.get('StudyInstanceUID', 'Unknown')
    study_date_str = ds.get('StudyDate', None)
    study_date = datetime.strptime(study_date_str, '%Y%m%d').date() if study_date_str else None

    # Generate a DICOMweb URL for the file
    dicom_url = f"http://localhost:8000/dicom-web/studies/{study_id}"  # Update to your DICOMweb URL

    # Save the DICOM image
    study, created = Study.objects.get_or_create(study_id=study_id, defaults={
        'patient_name': patient_name,
        'patient_id': patient_id,
        'birth_date': birth_date,
        'gender': gender,
        'study_date': study_date,
        'study_description': study_description,
    })

    dicom_image = DICOMImage(file=uploaded_file,
                             patient_id=patient_id,
                             patient_name=patient_name,
                             birth_date=birth_date,
                             modality=modality,
                             body_part=body_part,
                             study=study,
                             dicom_url=dicom_url)
    dicom_image.save()



    
# Helper function to normalize pixel data
def normalize_pixel_array(pixel_array):
    pixel_array = np.clip(pixel_array, pixel_array.min(), pixel_array.max())
    pixel_array = (pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min())
    pixel_array = (pixel_array * 255).astype(np.uint8)
    return pixel_array

# Function to adjust window level and width
def adjust_window_level(pixel_array, window_center, window_width):
    min_intensity = window_center - (window_width / 2)
    max_intensity = window_center + (window_width / 2)
    pixel_array = np.clip(pixel_array, min_intensity, max_intensity)
    pixel_array = (pixel_array - min_intensity) / (max_intensity - min_intensity) * 255
    return pixel_array.astype(np.uint8)


def delete_dicom_instance(request, instance_id):
    dicom_instance = get_object_or_404(DICOMImage, pk=instance_id)
    study_pk = dicom_instance.study.pk  # Save the study ID before deletion
    if request.method == 'POST':
        dicom_instance.delete()
        messages.success(request, 'DICOM instance deleted successfully.')
        return redirect('dicom:detail', pk=study_pk)
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('dicom:detail', pk=study_pk)

# dicom/views.py

def detail_view(request, pk):
    study = get_object_or_404(Study, pk=pk)
    study_form = StudyDetailForm(instance=study)
    report_form = ReportForm(instance=study)
    document_form = AdditionalDocumentForm()

    if request.method == 'POST':
        if 'save_study_details' in request.POST:
            study_form = StudyDetailForm(request.POST, instance=study)
            if study_form.is_valid():
                study_form.save()
                messages.success(request, 'Study details updated successfully.')
                return redirect('dicom:detail', pk=pk)
            else:
                messages.error(request, 'Error updating study details. Please check the form.')

        elif 'save_report' in request.POST:
            report_form = ReportForm(request.POST, instance=study)
            if report_form.is_valid():
                report_form.save()
                messages.success(request, 'Report updated successfully.')
                return redirect('dicom:detail', pk=pk)
            else:
                messages.error(request, 'Error updating report. Please check the form.')

        elif 'upload_document' in request.POST:
            document_form = AdditionalDocumentForm(request.POST, request.FILES)
            if document_form.is_valid():
                new_document = document_form.save(commit=False)
                new_document.study = study
                new_document.save()
                messages.success(request, 'Document uploaded successfully.')
                return redirect('dicom:detail', pk=pk)
            else:
                messages.error(request, 'Error uploading document. Please check the form.')

    # Fetch DICOM images associated with the study
    images = study.images.all()

    return render(request, 'dicom/detail.html', {
        'study': study,
        'study_form': study_form,
        'report_form': report_form,
        'document_form': document_form,
        'images': images,
    })






# dicom/views.py


def dicom_list_view(request):
    query = request.GET.get('q')
    if query:
        studies = Study.objects.filter(patient_name__icontains=query).prefetch_related('images')
    else:
        studies = Study.objects.prefetch_related('images').all()

    paginator = Paginator(studies, 25)  # Show 25 studies per page
    page = request.GET.get('page', 1)

    try:
        studies = paginator.page(page)
    except PageNotAnInteger:
        studies = paginator.page(1)
    except EmptyPage:
        studies = paginator.page(paginator.num_pages)

    assign_form = AssignStudyForm()
    return render(request, 'dicom/dicom_list.html', {'studies': studies, 'assign_form': assign_form})

def assign_study(request, study_id):
    if request.method == 'POST':
        form = AssignStudyForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            study = get_object_or_404(Study, pk=study_id)
            study.assigned_doctor = doctor  # Assuming you have an assigned_doctor field in Study model
            study.save()
            messages.success(request, f"Study {study.study_id} assigned to {doctor.user.username}.")
            return redirect('dicom:dicom_list')
        else:
            messages.error(request, "Error in form submission.")
    return redirect('dicom:dicom_list')



def download_report(request, pk):
    study = get_object_or_404(Study, pk=pk)
    context = {'study': study}
    pdf = generate_pdf('dicom/report_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{study.patient_name}_report.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

def generate_pdf(template_src, context_dict):
    template = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def convert_dicom_to_png(dicom_file_path, output_file_path):
    itk_image = sitk.ReadImage(dicom_file_path)
    pixel_array = sitk.GetArrayFromImage(itk_image)

    if pixel_array.ndim == 3:
        pixel_array = pixel_array[0]  # Take the first frame if it's a multi-frame DICOM

    pixel_array = normalize_pixel_array(pixel_array)

    buf = io.BytesIO()
    plt.imsave(buf, pixel_array, cmap='gray', format='png')
    buf.seek(0)

    with open(output_file_path, 'wb') as f:
        f.write(buf.getvalue())

# dicom/views.py


def view_image(request, image_id):
    dicom_image = get_object_or_404(DICOMImage, pk=image_id)
    dicom_file_path = dicom_image.file.path
    output_file_path = os.path.join('media', 'dicom_images', f'{image_id}.png')

    try:
        convert_dicom_to_png(dicom_file_path, output_file_path)
    except Exception as e:
        return HttpResponse(f"Error converting DICOM file: {e}", status=500)

    image_url = request.build_absolute_uri(f'/{output_file_path.replace("\\", "/")}')

    context = {
        'image_id': image_id,
        'image_url': image_url,
    }

    return render(request, 'dicom/view_image.html', context)





def get_annotations(request, image_id):
    dicom_image = get_object_or_404(DICOMImage, pk=image_id)
    annotations = json.loads(request.POST.get('annotations', '[]'))

    context = {
        'annotations': annotations
    }

    return JsonResponse(context)

def measure_distance(request, image_id):
    dicom_image = get_object_or_404(DICOMImage, pk=image_id)
    points = json.loads(request.POST.get('points', '[]'))

    distances = []
    for point in points:
        x1, y1, x2, y2 = point
        distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distances.append(distance)

    return JsonResponse({'distances': distances})

def compare_images(request):
    image_ids = request.GET.getlist('image_ids')
    images = [get_object_or_404(DICOMImage, pk=image_id) for image_id in image_ids]

    pixel_arrays = []
    for image in images:
        dicom_file_path = image.file.path
        itk_image = sitk.ReadImage(dicom_file_path)
        pixel_array = sitk.GetArrayFromImage(itk_image)
        pixel_arrays.append(pixel_array.tolist())

    return JsonResponse({'images': pixel_arrays})




def export_image(request, image_id, format):
    dicom_image = get_object_or_404(DICOMImage, pk=image_id)
    dicom_file_path = dicom_image.file.path
    output_format = format.lower()

    itk_image = sitk.ReadImage(dicom_file_path)
    pixel_array = sitk.GetArrayFromImage(itk_image)

    if pixel_array.ndim == 3:
        pixel_array = pixel_array[0]  # Take the first frame if it's a multi-frame DICOM

    buf = io.BytesIO()
    plt.imsave(buf, pixel_array, cmap='gray', format=output_format)
    buf.seek(0)

    response = HttpResponse(buf, content_type=f'image/{output_format}')
    response['Content-Disposition'] = f'attachment; filename="image_{image_id}.{output_format}"'
    return response

def load_image_series(request, study_id):
    study = get_object_or_404(DICOMStudy, pk=study_id)
    series = [{'id': series.id, 'description': series.description} for series in study.series_set.all()]
    return JsonResponse({'series': series})

def image_stacking(request, study_id):
    study = get_object_or_404(DICOMStudy, pk=study_id)
    stack = [{'id': image.id, 'file': image.file.url} for series in study.series_set.all() for image in series.images.all()]
    return JsonResponse({'stack': stack})
