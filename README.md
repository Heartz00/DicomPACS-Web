# Alegria PACS website
**Built by @Heartz00 - Ayomide Oladele**

Note: that this solution is still subject to improvement.
A full-featured Picture Archiving and Communication System (PACS) website built using Django Python framework.

Overview

DicomPACS-Web is a web-based PACS system designed to store, manage, and analyze DICOM images. The system allows doctors to upload, view, and write reports on DICOM images, as well as extract relevant information from the images.

Features

- DICOM Image Storage: Store and manage DICOM images in a centralized database.
- Image Viewer: View DICOM images in a web-based viewer with zoom, pan, and windowing capabilities.
- Report Writing: Allow doctors to write reports on DICOM images, including text, images, and other relevant information.
- DICOM Tag Extraction: Extract relevant information from DICOM images, such as patient name, study date, and image modality.
- User Management: Manage user accounts, roles, and permissions.

Technical Details

- Framework: Django Python framework
- Database: Sqlite
- DICOM Library: Pydicom
- Frontend: HTML, CSS, JavaScript, Bootstrap

Installation

1. Clone the repository: `git clone https://github.com/Heartz00/DicomPACS-Web.git'🍡 
2. Navigate to the directory where the clone repo is and Install dependencies: pip install -r requirements.txt
3. Run migrations in the directory of the main folder: python manage.py migrate
4. Start the server: python manage.py runserver

Contributing

Contributions are welcome! Please submit a pull request with your changes.
