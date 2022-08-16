import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycore.tikz as tikz
import pycore.blocks as blocks
import pycore.execute as execute


def create_architecture():
    input = 40
    base_width = 64
    arch = []
    arch += tikz.start()
    arch += tikz.image(name='image_0', file='\\input_image', to=('-3,0,0'), size=(10, 10))
    arch += blocks.conv_relu(name='conv_0_0', prev='0,0,0', z_label='I',
                             size=(input, input), n_filter=64, anchor='', conn=False)
    arch += tikz.short_connection(of='image_0', to='conv_0_0', anchor_of='', fill='')
    arch += blocks.conv_relu(name='conv_0_1', prev='conv_0_0', z_label='I/2',
                             size=(input / 2, input / 2), n_filter=64, offset=(2, 0, 0), conn=False)
    arch += tikz.short_connection(of='conv_0_0', to='conv_0_1', fill='')
    arch += tikz.resample('conv_0_0', 'conv_0_1')
    arch += blocks.conv_relu(name='conv_1_0', prev='conv_0_1', z_label='I/4',
                             size=(input / 4, input / 4), n_filter=64, offset=(2, 0, 0))
    arch += tikz.resample('conv_0_1', 'conv_1_0')
    arch += blocks.multi_conv_relu(num=3, name='conv_1', prev='conv_1_0', name_start=1,
                                   n_filter=[64, 64, 256], size=(input / 4, input / 4),
                                   offset=(1.5, 0, 0))
    arch += blocks.tikz.long_connection('conv_1_0', 'conv_1_3', pos=1.5, anchor_to='-northeast')

    # Stage 2

    # branch 0
    arch += blocks.conv_relu('conv_2_0_0', prev='conv_1_3', n_filter=base_width, conn=False, size=input / 4,
                             offset=(1.25, 0, 0))
    arch += tikz.ellipsis('conv_1_3', 'conv_2_0_0')
    arch += blocks.multi_conv_relu(num=2, name='conv_2_0', prev='conv_2_0_0', name_start=1,
                                   n_filter=base_width, size=input / 4, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_0', prev='conv_2_0_2', name_start=3,
                                   n_filter=base_width, size=input / 4, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_0', prev='conv_2_0_4', name_start=5,
                                   n_filter=base_width, size=input / 4, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_0', prev='conv_2_0_6', name_start=7,
                                   n_filter=base_width, size=input / 4, offset=(1.25, 0, 0))
    # branch 1
    arch += blocks.new_branch(name='conv_2_1_0', prev='conv_2_0_0', n_filter=base_width * 2,
                              offset=(2, 0, 8), size=input / 8, anchor='-west', z_label='I/8')
    arch += blocks.multi_conv_relu(num=2, name='conv_2_1', prev='conv_2_1_0', name_start=1,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_1', prev='conv_2_1_2', name_start=3,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_1', prev='conv_2_1_4', name_start=5,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.25, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_2_1', prev='conv_2_1_6', name_start=7,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.25, 0, 0))
    
    # Fuse
    arch += blocks.sum(name='sum_2_0', prev='conv_2_0_8', offset=(2, 0, 0))
    arch += blocks.sum(name='sum_2_1', prev='conv_2_1_8', offset=(2, 0, 0))
    arch += tikz.fuseconnection('conv_2_0_8', 'sum_2_1', anchor_to='-northnorthwest')
    arch += tikz.fuseconnection('conv_2_1_8', 'sum_2_0', anchor_to='-southsouthwest')

    # Stage 3

    # branch 0
    # arch += blocks.multi_conv_relu(num=2, name='conv_3_0', prev='sum_2_0', name_start=1,
    #                                n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))

    # branch 0
    arch += blocks.multi_conv_relu(num=2, name='conv_3_0', prev='sum_2_0', name_start=1,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_0', prev='conv_3_0_2', name_start=3,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_0', prev='conv_3_0_4', name_start=5,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_0', prev='conv_3_0_6', name_start=7,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    # branch 1
    arch += blocks.multi_conv_relu(num=2, name='conv_3_1', prev='sum_2_1', name_start=1,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_1', prev='conv_3_1_2', name_start=3,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_1', prev='conv_3_1_4', name_start=5,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_1', prev='conv_3_1_6', name_start=7,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    # branch 2
    arch += blocks.new_branch(name='conv_3_2_0', prev='sum_2_1', n_filter=base_width * 4,
                              offset=(1.5, 0, 6), size=input / 16, anchor='-south', z_label='I/16')
    arch += blocks.multi_conv_relu(num=2, name='conv_3_2', prev='conv_3_2_0', name_start=1,
                                   n_filter=base_width * 4, size=input / 16, offset=(1.2, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_2', prev='conv_3_2_2', name_start=3,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_2', prev='conv_3_2_4', name_start=5,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_3_2', prev='conv_3_2_6', name_start=7,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))

    # Fuse
    arch += blocks.sum(name='sum_3_0', prev='conv_3_0_8', offset=(2.5, 0, 0))
    arch += blocks.sum(name='sum_3_1', prev='conv_3_1_8', offset=(2.5, 0, 0))
    arch += blocks.sum(name='sum_3_2', prev='conv_3_2_8', offset=(2.5, 0, 0))
    arch += tikz.fuseconnection('conv_3_0_8', 'sum_3_1', anchor_to='-northwest')
    arch += tikz.fuseconnection('conv_3_0_8', 'sum_3_2', anchor_to='-north')
    arch += tikz.fuseconnection('conv_3_1_8', 'sum_3_0', anchor_to='-southwest')
    arch += tikz.fuseconnection('conv_3_1_8', 'sum_3_2', anchor_to='-northwest')
    arch += tikz.fuseconnection('conv_3_2_8', 'sum_3_0')
    arch += tikz.fuseconnection('conv_3_2_8', 'sum_3_1', anchor_to='-southwest')
    arch += tikz.short_connection(of='conv_3_1_8', to='sum_3_1')

    # Stage 4

    # branch 0
    arch += blocks.multi_conv_relu(num=2, name='conv_4_0', prev='sum_3_0', name_start=1,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_0', prev='conv_4_0_2', name_start=3,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_0', prev='conv_4_0_4', name_start=5,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_0', prev='conv_4_0_6', name_start=7,
                                   n_filter=base_width, size=input / 4, offset=(1.35, 0, 0))
    # branch 1
    arch += blocks.multi_conv_relu(num=2, name='conv_4_1', prev='sum_3_1', name_start=1,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_1', prev='conv_4_1_2', name_start=3,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_1', prev='conv_4_1_4', name_start=5,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_1', prev='conv_4_1_6', name_start=7,
                                   n_filter=base_width * 2, size=input / 8, offset=(1.15, 0, 0))
    # branch 2
    arch += blocks.multi_conv_relu(num=2, name='conv_4_2', prev='sum_3_2', name_start=1,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_2', prev='conv_4_2_2', name_start=3,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_2', prev='conv_4_2_4', name_start=5,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_2', prev='conv_4_2_6', name_start=7,
                                   n_filter=base_width * 4, size=input / 16, offset=(1, 0, 0))

    # branch 3
    arch += blocks.new_branch(name='conv_4_3_0', prev='sum_3_2', n_filter=base_width * 8,
                              offset=(1.5, 0, 6), size=input / 32, anchor='-south', z_label='I/32')
    arch += blocks.multi_conv_relu(num=2, name='conv_4_3', prev='conv_4_3_0', name_start=1,
                                   n_filter=base_width * 8, size=input / 32, offset=(0.9, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_3', prev='conv_4_3_2', name_start=3,
                                   n_filter=base_width * 8, size=input / 32, offset=(0.9, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_3', prev='conv_4_3_4', name_start=5,
                                   n_filter=base_width * 8, size=input / 32, offset=(0.9, 0, 0))
    arch += blocks.multi_conv_relu(num=2, name='conv_4_3', prev='conv_4_3_6', name_start=7,
                                   n_filter=base_width * 8, size=input / 32, offset=(0.9, 0, 0))

    arch += blocks.sum(name='sum_4_0', prev='conv_4_0_8', offset=(3.5, 0, 0))
    arch += blocks.sum(name='sum_4_1', prev='conv_4_1_8', offset=(3.5, 0, 0))
    arch += blocks.sum(name='sum_4_2', prev='conv_4_2_8', offset=(3.5, 0, 0))
    arch += blocks.sum(name='sum_4_3', prev='conv_4_3_8', offset=(3.5, 0, 0))
    arch += tikz.fuseconnection('conv_4_0_8', 'sum_4_1', anchor_to='-northnorthwest')
    arch += tikz.fuseconnection('conv_4_0_8', 'sum_4_2', anchor_to='-northwest')
    arch += tikz.fuseconnection('conv_4_0_8', 'sum_4_3', anchor_to='-north')
    arch += tikz.fuseconnection('conv_4_1_8', 'sum_4_0', anchor_to='-southwest')
    arch += tikz.fuseconnection('conv_4_1_8', 'sum_4_2', anchor_to='-northwest')
    arch += tikz.fuseconnection('conv_4_1_8', 'sum_4_3', anchor_to='-northnorthwest')
    arch += tikz.fuseconnection('conv_4_2_8', 'sum_4_0', anchor_to='-southsouthwest')
    arch += tikz.fuseconnection('conv_4_2_8', 'sum_4_1', anchor_to='-southwest')
    arch += tikz.fuseconnection('conv_4_2_8', 'sum_4_3', anchor_to='-northwest')
    arch += tikz.fuseconnection('conv_4_3_8', 'sum_4_0')
    arch += tikz.fuseconnection('conv_4_3_8', 'sum_4_1', anchor_to='-southwest')
    arch += tikz.fuseconnection('conv_4_3_8', 'sum_4_2', anchor_to='-southsouthwest')
    arch += tikz.short_connection(of='conv_4_1_8', to='sum_4_1')
    arch += tikz.short_connection(of='conv_4_2_8', to='sum_4_2')

    # arch += blocks.conc('conc_0', 'sum_4_0', offset=(2, 0, 0))
    # arch += tikz.short_connection('sum_4_1', 'conc_0', anchor_of='-east', anchor_to='-southwest')
    # arch += tikz.short_connection('sum_4_2', 'conc_0', anchor_of='-east', anchor_to='-southsouthwest')
    # arch += tikz.short_connection('sum_4_3', 'conc_0', anchor_of='-east', anchor_to='-south')

    arch += blocks.conv_relu(name='conv_5_3', prev='sum_4_3',
                             size=input / 32, n_filter=256)
    arch += blocks.upsample('up_5_3', prev='conv_5_3', size=input / 16)
    arch += blocks.conv_relu(name='conv_5_2', prev='sum_4_2', offset=(4, 0, 0),
                             size=input / 16, n_filter=256)
    arch += blocks.sum(name='sum_5_2', prev='conv_5_2', offset=(1.5, 0, 0))
    arch += tikz.z_connection('up_5_3', 'sum_5_2', shift=(1,0,0), anchor_of='-west', anchor_to='-south')
    arch += blocks.upsample('up_5_2', prev='sum_5_2', size=input / 8)

    arch += blocks.conv_relu(name='conv_5_1', prev='sum_4_1', offset=(6, 0, 0),
                             size=input / 8, n_filter=256)
    arch += blocks.sum(name='sum_5_1', prev='conv_5_1', offset=(4.5, 0, 0))
    arch += tikz.z_connection('up_5_2', 'sum_5_1', anchor_of='-west', anchor_to='-south')
    arch += blocks.upsample('up_5_1', prev='sum_5_1', size=input / 4, offset=(1.5,0,0))
    arch += blocks.conv_relu(name='conv_5_0', prev='sum_4_0', offset=(8, 0, 0),
                             size=input / 4, n_filter=256)
    arch += blocks.sum(name='sum_5_0', prev='conv_5_0', offset=(8.5, 0, 0))
    arch += tikz.z_connection('up_5_1', 'sum_5_0', anchor_of='-west', anchor_to='-south')

    arch += blocks.conv_relu(name='conv_5_0_1', prev='sum_5_0', offset=(2.5, 0, 0),
                             size=input / 4, n_filter='43', width=2.5)
    arch += tikz.soft_max('soft_max', offset=(2, 0, 0), to='conv_5_0_1-east', size=(input / 4, input / 4), 
                          n_filter=32)
    arch += tikz.short_connection('conv_5_0_1', 'soft_max')
    arch += tikz.image(name='image_1', file='\\output_image', to='soft_max-east', size=(2.5, 2.5), x_shift=2)
    arch += tikz.short_connection('soft_max', 'image_1', anchor_to='')
    arch += tikz.image(name='image_2', file='\\output_image', to='image_1.east', size=(10, 10), x_shift=3)
    arch += tikz.resample('image_1', 'image_2')


    # Close environment
    arch += tikz.env_end()
    return arch

def main():
    pdf = False
    namefile = str(sys.argv[0]).split('.')[0]
    arch = create_architecture()
    # to_Generate(arch, namefile + '.tex')
    content = execute.build_architecture(arch)
    execute.write_tex(content, namefile + ".tex")
    if pdf:
        execute.tex_to_pdf(namefile + ".tex")
        if sys.platform.startswith('linux'):
            execute.open_pdf('xdg-open', os.path.join(namefile + '.pdf'))
        elif sys.platform.startswith('win32'):
            os.startfile(os.path.join(namefile + '.pdf'))


if __name__ == '__main__':
    main()
