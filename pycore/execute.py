import sys
import subprocess
import os

def call_process(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def delete_files(pattern):
    cmd = "rm"
    if os.name == 'nt':
        cmd = "del"
    cmd += " " + pattern
    call_process(cmd)

def open_pdf(tool, pdf="file.pdf"):
    try:
        call_process(tool + " " + pdf)
    except subprocess.CalledProcessError:
        print('Error while trying to open pdf viewer')

def tex_to_pdf(file="file.tex", folder='output', delete_tmp=True):
    os.chdir(folder)
    call_process('pdflatex ' + str(file))
    if delete_tmp:
        delete_files("*.aux *.log")
    os.chdir('..')

def write_tex(content, file="file.tex"):
    with open(file, "w") as f:
        f.write(str(content))

def build_architecture(arch):
    content = ""
    for c in arch:
        content += str(c)
    return content
