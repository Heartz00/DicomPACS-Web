# dicom/urls.py


from django.urls import path
from dicom.views import upload_view, delete_dicom_instance, detail_view, export_image, load_image_series, image_stacking, dicom_list_view, download_report, assign_study, view_image

app_name = 'dicom'

urlpatterns = [
    path('upload/', upload_view, name='upload'),
    path('detail/<int:pk>/', detail_view, name='detail'),
    path('list/', dicom_list_view, name='dicom_list'),
    path('report/download/<int:pk>/', download_report, name='download_report'),
    path('assign_study/<int:study_id>/', assign_study, name='assign_study'),
    path('view_image/<int:image_id>/', view_image, name='view_image'),  # Ensure this line is added
    path('export_image/<int:image_id>/<str:format>/', export_image, name='export_image'),
    path('load_image_series/<int:study_id>/', load_image_series, name='load_image_series'),
    path('image_stacking/<int:study_id>/', image_stacking, name='image_stacking'),
    path('delete-instance/<int:instance_id>/', delete_dicom_instance, name='delete_dicom_instance'),



]
