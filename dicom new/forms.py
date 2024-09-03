from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('upload/', views.upload_dicom, name='upload_dicom'),
]

