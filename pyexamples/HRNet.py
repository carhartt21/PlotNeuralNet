import sys
sys.path.append('../')
import pycore.tikz as tikz
import pycore.blocks as blocks
import pycore.execute as execute


def create_architecture():
    arch = blocks.conv_pool()
    return arch
def main():
    try:
        namefile = str(sys.argv[0]).split('.')[0]
        arch = create_architecture()
        # to_Generate(arch, namefile + '.tex')
        content = execute.build_architecture(arch)
        execute.write_tex(content, namefile + ".tex")
        execute.tex_to_pdf(namefile + ".tex")
        execute.openPDF("xdg-open", namefile + ".pdf")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
    main()
