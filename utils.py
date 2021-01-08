# utilities
import os
from re import sub
import uuid
import subprocess

# Image To Pdf
import img2pdf


_BASE_DIR = os.getcwd() 
_BASE_DIR_FILE = os.path.join(_BASE_DIR, "files")


def process_image_to_pdf(files, pdf_name):
    img = []
    with open(f"{_BASE_DIR_FILE}/{pdf_name}.pdf","wb") as fil:
        for fname in files:
            path = os.path.join(_BASE_DIR_FILE, fname)
            img.append(path)
        fil.write(img2pdf.convert(img))
    return pdf_name

def process_word_to_pdf(file):
    file_address = os.path.join(_BASE_DIR_FILE, file)
    command = ['lowriter' ,'--convert-to','pdf' , file_address , "--outdir", _BASE_DIR_FILE]
    command_run = subprocess.run(command)
    file_name = -1
    if command_run.returncode == 0:
        file_name = ".".join(file.split(".")[:-1]) + ".pdf"
    return file_name


def del_user_files(list):
    for file in list:
        file_address = os.path.join(_BASE_DIR_FILE, file)
        try:
            os.remove(file_address)
        except:
            pass


def del_one_file(file):
    try:
        os.remove(file)
    except:
        try:
            file_address = os.path.join(_BASE_DIR_FILE, file)
            os.remove(file_address)
        except:
            pass
        pass
    return 1