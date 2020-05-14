import sys
import os
sys.path.append('..')
import pycore.tikz as tikz
import pycore.blocks as blocks
import pycore.execute as execute


def create_architecture():
    arch = []
    arch += tikz.start()
    arch += tikz.image(name='image_0', file='\\input_image', to=('-4,0,0'), size=(10, 10))
    arch += blocks.conv_relu(name='conv_0', prev='0,0,0', anchor='')
    arch += tikz.env_end()
    return arch

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = create_architecture()
    # to_Generate(arch, namefile + '.tex')
    content = execute.build_architecture(arch)
    execute.write_tex(content, namefile + ".tex")
    execute.tex_to_pdf(namefile + ".tex")
    if sys.platform.startswith('linux'):
        execute.open_pdf('xdg-open', os.path.join(namefile + '.pdf'))
    elif sys.platform.startswith('win32'):
        os.startfile(os.path.join(namefile + '.pdf'))


if __name__ == '__main__':
    main()
