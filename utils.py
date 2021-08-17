# utilities
import os
from re import sub
import uuid
import subprocess

# Image To Pdf
import img2pdf

# PDF To Images
from pdf2image import convert_from_path

# PDF To Word
from pdf2docx import parse


_BASE_DIR = os.getcwd() 
_BASE_DIR_FILE = os.path.join(_BASE_DIR, "files")


def process_image_to_pdf(files):
    img = []
    tmp = [] 
    for fname in files:
        path = os.path.join(_BASE_DIR_FILE, fname)
        tmp.append(path)
        if len(tmp) == 50:
            img.append(tmp)
            tmp = []
    if tmp:
        img.append(tmp)
    pdf_names = [
        str(uuid.uuid1()) for _ in range(len(img))
    ]
    for i,j in zip(img, pdf_names):
        try:
            with open(f"{_BASE_DIR_FILE}/{j}.pdf","wb") as fil:
                fil.write(img2pdf.convert(i))
        except:
            pass
        
    return pdf_names

def process_word_to_pdf(file):
    file_address = os.path.join(_BASE_DIR_FILE, file)
    command = ['lowriter' ,'--convert-to','pdf' , file_address , "--outdir", _BASE_DIR_FILE]
    command_run = subprocess.run(command)
    file_name = -1
    if command_run.returncode == 0:
        file_name = ".".join(file.split(".")[:-1]) + ".pdf"
    return file_name


def process_pdf_to_images(file):
    file_address = os.path.join(_BASE_DIR_FILE, file)
    folder_name = str(uuid.uuid1())
    folder_address = os.path.join(_BASE_DIR_FILE, folder_name)
    os.mkdir(folder_address)
    try:
        convert_from_path(file_address, output_folder=folder_address, fmt="jpeg", thread_count=10, jpegopt="quality")
        return folder_address
    except:
        import shutil
        shutil.rmtree(folder_address)
        return -1

def process_pdf_to_word(file):
    file_address = os.path.join(_BASE_DIR_FILE, file)
    word_file = str(uuid.uuid1()) + ".docx"
    word_file_address = os.path.join(_BASE_DIR_FILE, word_file)
    try:  
        parse(file_address, word_file_address, multi_processing=True)
        return word_file_address
    except:
        return -1

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