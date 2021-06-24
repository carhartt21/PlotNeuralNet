import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycore.tikz as tikz
import pycore.blocks as blocks
import pycore.execute as execute


def create_architecture():
    input = 32
    base_width = 64
    
    arch = []
    arch += tikz.start()
    arch += tikz.image(name='image_0', file='\\input_image', to=('-4,0,0'), size=(10, 10))
    arch += blocks.conv_relu(name='conv_1', prev='0,0,0', z_label='I',
                             size=(input, input), n_filter=3, anchor='', conn=False)
    # arch += tikz.short_connection(of='image_0', to='conv_1', anchor_of='.center', fill='')
    # arch += tikz.resample('image_0', 'conv_1')

    arch += tikz.pool(name='pool_1', width=1, to='conv_1', size=(input, input),
                      offset=(3, 0, 0))
    arch += tikz.short_connection(of='conv_1', to='pool_1', fill='')

    arch += blocks.conv_relu(name='conv_2', prev='pool_1', z_label='I/2',
                         size=(input / 2, input / 2), n_filter=96, offset=(2, 0, 0), conn=False)
    arch += tikz.resample('pool_1', 'conv_2')
    arch += tikz.short_connection(of='pool_1', to='conv_2', fill='')

    arch += tikz.pool(name='pool_2', width=1, to='conv_2', size=(input / 2, input / 2),
                      offset=(2, 0, 0))
    arch += tikz.short_connection(of='conv_2', to='pool_2', fill='')

    # arch += blocks.conv_relu(name='conv_3', prev='pool_2', z_label='I/4',
    #                          size=(input / 4, input / 4), n_filter=256, offset=(1, 0, 0), conn=False)

    arch += blocks.multi_conv_relu(num=3, name='conv_4_6', prev='pool_2', z_label='I/4',
                             size=(input / 4, input / 4), n_filter=[384, 384, 256], offset=(2, 0, 0), conn=False)    

    arch += tikz.short_connection(of='pool_2', to='conv_4_6_0', fill='')
    arch += tikz.resample('pool_2', 'conv_4_6_0')

    arch += tikz.pool(name='pool_3', width=1, to='conv_4_6_2', size=(input / 4, input / 4),
                      offset=(1, 0, 0))
    arch += tikz.short_connection(of='conv_4_6_2', to='pool_3', fill='')

    arch += tikz.full_con(name='fully_1', n_filter=4096, size=(input / 8, input / 8), to='pool_3-east', offset=(1, 0))
    arch += tikz.short_connection(of='pool_3', to='fully_1', fill='')
    arch += tikz.resample('pool_3', 'fully_1')

    arch += tikz.full_con(name='fully_2', n_filter=4096, size=(input / 8, input / 8), to='fully_1-east', offset=(1, 0))
    arch += tikz.full_connection('fully_1', 'fully_2')
    arch += tikz.full_con(name='fully_3', n_filter=40, size=(input / 8, input / 8), to='fully_2-east', offset=(1, 0))
    arch += tikz.full_connection('fully_2', 'fully_3')

    arch += tikz.soft_max('soft_max', offset=(2, 0, 0), to='fully_3', size=(input / 8, input / 8),
                          n_filter=40, anchor_to='-west')
    arch += tikz.short_connection(of='fully_3', to='soft_max', fill='')

                    
    # arch += tikz.short_connection('conv_68', 'soft_max', anchor_of='-west', anchor_to='-east')    
    # arch += tikz.results_upsampling()
    # arch += tikz.spatial_mask()
    # arch += tikz.legend()
    # arch += tikz.resample('image_1', 'image_2')

    # arch += tikz.short_connection(of='conv_61', to='sum_1', anchor_of='-east',
    #                               anchor_to='-west')
    # arch += tikz.resample('image_1', 'image_2')

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
