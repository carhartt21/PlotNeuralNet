import sys, subprocess, os

def callProcessWithCommand(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deleteFiles(files):
    Cmd = "rm"
    if os.name == 'nt':
        Cmd = "del"
    Cmd += " " + files
    callProcessWithCommand(Cmd)

def openPDF(tool, pdf="file.pdf"):
    callProcessWithCommand(tool + " " + pdf)

def texToPDF(tex="file.tex", deleteTmpFiles=True):
    callProcessWithCommand('pdflatex ' + str(tex))
    if deleteTmpFiles:
        deleteFiles("*.aux *.log")

def writeTex(content, file = "file.tex"):
    with open(file, "w") as f:
        f.write(str(content))

def buildArchitecture(arch):
    content = ""
    for c in arch:
        content += str(c)
    return content
