import sys
sys.path.append('../')
import pycore.tikz as tikz
import pycore.blocks as blocks
import pycore.execute as execute


def creat_architecture():
    arch = blocks.conv_pool()
    return arch
def main():
    try:
        namefile = str(sys.argv[0]).split('.')[0]
        arch = creat_architecture()
        # to_Generate(arch, namefile + '.tex')
        content = execute.buildArchitecture(arch)
        execute.writeTex(content, namefile + ".tex")
        execute.texToPDF(namefile + ".tex")
        execute.openPDF("xdg-open", namefile + ".pdf")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
    main()
