import subprocess
import os

def convert_docx_to_pdf(docx_path, pdf_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path, '--outdir', os.path.dirname(pdf_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return False
    return True