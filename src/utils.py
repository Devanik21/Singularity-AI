import os
import tempfile
import zipfile
import streamlit as st
from typing import Dict

def create_project_files(project_data: Dict, base_path: str):
    """Create actual files from project data"""
    # Ensure base directory exists
    os.makedirs(base_path, exist_ok=True)

    for filename, content in project_data["files"].items():
        file_path = os.path.join(base_path, filename)

        # Create directory if filename contains subdirectories
        file_dir = os.path.dirname(file_path)
        if file_dir and file_dir != base_path:
            os.makedirs(file_dir, exist_ok=True)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            st.error(f"Failed to create file {filename}: {str(e)}")
            continue

def create_zip_download(project_data: Dict) -> bytes:
    """Create downloadable zip file"""
    zip_buffer = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')

    with zipfile.ZipFile(zip_buffer.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in project_data["files"].items():
            zip_file.writestr(filename, content)

    with open(zip_buffer.name, 'rb') as f:
        zip_data = f.read()

    os.unlink(zip_buffer.name)
    return zip_data
