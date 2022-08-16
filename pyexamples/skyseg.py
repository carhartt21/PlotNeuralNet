from cProfile import label
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
    # arch += tikz.image(name='image_0', file='\\input_image', to=('-3,0,0'), size=(10, 10))
    # arch += blocks.conv_relu(name='conv_0_0', prev='0,0,0', z_label='I',
    #                          size=(input, input), n_filter=64, anchor='', conn=False)
    # arch += tikz.short_connection(of='image_0', to='conv_0_0', anchor_of='', fill='')
    # arch += blocks.conv_relu(name='conv_0_1', prev='conv_0_0', z_label='I/2',
    #                          size=(input / 2, input / 2), n_filter=64, offset=(2, 0, 0), conn=False)
    # arch += tikz.short_connection(of='conv_0_0', to='conv_0_1', fill='')
    # arch += tikz.resample('conv_0_0', 'conv_0_1')
    # arch += blocks.conv_relu(name='conv_1_0', prev='conv_0_1', z_label='I/4',
    #                          size=(input / 4, input / 4), n_filter=64, offset=(1, 0, 0), conn=False)
    # arch += tikz.short_connection(of='conv_0_1', to='conv_1_0', fill='')
    # arch += tikz.resample('conv_0_1', 'conv_1_0')

    # arch += tikz.pool(name='pool_0', width=2, to='conv_1_0', size=(input / 4, input / 4),
    #                   offset=(1, 0, 0))

    # arch += tikz.short_connection(of='conv_1_0', to='pool_0', fill='')

    # arch += blocks.multi_conv_relu(num=3, name='conv_1', prev='conv_1_0', name_start=1,
    #                                n_filter=[64, 64, 256], size=(input / 4, input / 4),
    #                                offset=(1.5, 0, 0))
    # arch += blocks.tikz.long_connection('conv_1_0', 'conv_1_3', pos=1.5, anchor_to='-northeast')

    # arch += blocks.bottleneck(3, 'bottleneck_1', prev='pool_0', size=(input / 4, input / 4),
    #                           n_filter=[64, 64, 256], offset=(1.5, 0, 0), layer_num=5)
    # arch += blocks.bottleneck(3, 'bottleneck_2', prev='bottleneck_1_2', size=(input / 4, input / 4),
    #                           n_filter=[64, 64, 256], offset=(1.5, 0, 0), layer_num=8)
    # arch += blocks.bottleneck(3, 'bottleneck_3', prev='bottleneck_2_2', size=(input / 4, input / 4),
    #                           n_filter=[64, 64, 256], offset=(1.5, 0, 0), layer_num=11)
    # arch += blocks.bottleneck(3, 'bottleneck_4', prev='bottleneck_3_2', size=(input / 8, input / 8),
    #                           n_filter=[128, 128, 512], offset=(3, 0, 0), layer_num=14)
    # arch += blocks.bottleneck(3, 'bottleneck_7', prev='bottleneck_4_2', size=(input / 8, input / 8),
    #                           n_filter=[128, 128, 512], offset=(1.5, 0, 0), conn=False, ellipsis=True, layer_num=24)
    # arch += blocks.bottleneck(3, 'bottleneck_8', prev='bottleneck_7_2', size=(input / 16, input / 16),
    #                           n_filter=[256, 256, 1024], offset=(1.5, 0, 0), pos=2, layer_num=27)
    # arch += blocks.bottleneck(3, 'bottleneck_13', prev='bottleneck_8_2', size=(input / 16, input / 16),
    #                           n_filter=[256, 256, 1024], offset=(1.5, 0, 0), pos=2, conn=False, 
    #                           ellipsis=True, layer_num=43)
    # arch += blocks.bottleneck(3, 'bottleneck_14', prev='bottleneck_13_2', size=(input / 32, input / 32),
    #                           n_filter=[512, 512, 2048], offset=(1.5, 0, 0), pos=3, layer_num=46)
    # arch += blocks.bottleneck(3, 'bottleneck_16', prev='bottleneck_14_2', size=(input / 32, input / 32), layer_num=53,
    #                           n_filter=[512, 512, 2048], offset=(1.5, 0, 0), pos=3, conn=False, ellipsis=True)

    # arch += tikz.coordinate('resnet_last_dummy', of='bottleneck_16_2-east', offset=(3, 0, 0))
    # arch += tikz.coordinate('resnet_connection_dummy', of='resnet_last_dummy', offset=(0, 0, 6))
    # arch += tikz.short_connection(of='bottleneck_16_2', to='resnet_last_dummy',
    #                               anchor_to='')
    # arch += tikz.short_connection(to='resnet_connection_dummy', of='resnet_last_dummy',
    #                               anchor_to='', anchor_of='')


    arch += tikz.pool(name='pool_1', width=2, to='0,0,0',
                      size=(input / 4, input / 4), offset=(0, -5, 0), anchor='', caption='')
    arch += blocks.conv_relu(name='conv_pool_1', prev='pool_1',
                             offset=(2.5, 0, 0), size=(input / 32, input / 32),
                             n_filter=512,  conn=False, label=False)
    arch += tikz.short_connection(of='pool_1', to='conv_pool_1', options='pos=0.75')

    arch += tikz.pool(name='pool_2', width=2, to='pool_1', size=(input / 4, input / 4),
                      offset=(0, 0, 6), anchor='-center', caption='')
    arch += tikz.grid(name='grid_2', at='pool_2', steps=2)
    arch += blocks.conv_relu(name='conv_pool_2', prev='pool_2', offset=(2.5, 0, 0),
                             size=(input / 32, input / 32), n_filter=512, label=False)

    arch += tikz.pool(name='pool_3', width=2, to='pool_2', size=(input / 4, input / 4),
                      offset=(0, 0, 6), anchor='-center', caption='')
    arch += tikz.grid(name='grid_3', at='pool_3', steps=4)
    arch += blocks.conv_relu(name='conv_pool_3', prev='pool_3', offset=(2.5, 0, 0),
                             size=(input / 32, input / 32), n_filter=512,  conn=False, label=False)
    arch += tikz.short_connection(of='pool_3', to='conv_pool_3',
                                   options='pos=0.75')

    # arch += tikz.pool(name='pool_4', width=2, to='pool_3', size=(input / 4, input / 4),
    #                   offset=(0, 0, 6), anchor='-center', caption='')
    # arch += tikz.grid(name='grid_4', at='pool_4', steps=8)
    # arch += blocks.conv_relu(name='conv_pool_4', prev='pool_4', offset=(2.5, 0, 0),
    #                          size=(input / 32, input / 32), n_filter=512,  conn=False, label=False)
    # arch += tikz.short_connection(of='pool_4', to='conv_pool_4',
    #                                options='pos=0.75')

    arch += blocks.conc(name='conc_1', prev='pool_2', offset=(5, 0, 0), conn=False)

    arch += tikz.coordinate('dummy_pool_1', 'pool_1-east', (-2.5, 0, 0))
    arch += tikz.coordinate('dummy_pool_2', 'pool_2-east', (-2.5, 0, 0))
    arch += tikz.coordinate('dummy_pool_3', 'pool_3-east', (-2.5, 0, 0))
    arch += tikz.coordinate('input', 'dummy_pool_2', (-4, 0, 0))

    arch += tikz.short_connection('dummy_pool_2', 'dummy_pool_1', anchor_of='', anchor_to='')
    arch += tikz.short_connection('dummy_pool_2', 'dummy_pool_3', anchor_of='', anchor_to='')
    arch += tikz.short_connection('input', 'dummy_pool_2', anchor_of='', anchor_to='')

    # arch += tikz.coordinate('dummy_pool_4', 'pool_4-east', (-2.5, 0, 0))

    arch += tikz.short_connection('dummy_pool_1', 'pool_1', anchor_of='')
    arch += tikz.double_connection('dummy_pool_2', 'dummy_pool_2', 'pool_2', anchor_of='')
    arch += tikz.double_connection('dummy_pool_3', 'dummy_pool_3', 'pool_3', anchor_of='')
    # arch += tikz.double_connection('dummy_pool_4', 'dummy_pool_4', 'pool_4', anchor_of='')

    # arch += tikz.z_connection(of='resnet_last_dummy', to='dummy_pool_1', anchor_to='', shift=(6, 0, 0), anchor_of='')
    # arch += tikz.z_connection(of='conv_5_0_1', to='pool_2', anchor_of='-anchor', shift=(-1, -1.5, 2))
    # arch += tikz.short_connection(of='conv_5_0_1', to='pool_3', anchor_to='-south')
    # arch += tikz.z_connection(of='conv_5_0_1', to='pool_4', anchor_to='-north', shift=(0, 0, 0))

    arch += tikz.z_connection('conv_pool_1', 'conc_1', anchor_of='-east', anchor_to='-northeast', shift=(1.5, 0, 0))
    arch += tikz.z_connection('conv_pool_2', 'conc_1', anchor_of='-east', anchor_to='-west', shift=(0, 0, 0))
    arch += tikz.z_connection('conv_pool_3', 'conc_1', anchor_of='-east', anchor_to='-southwest', shift=(1.4, 0, 0))
    # arch += tikz.z_connection('conv_pool_4', 'conc_1', anchor_of='-east', anchor_to='-south', shift=(2, 0, 0))
    # arch += tikz.z_connection('resnet_connection_dummy', 'conc_1', anchor_of='',
    #                           anchor_to='-northwest', shift=(-4.5, 0, 0))

    arch += blocks.conv_relu(name='conv_60', prev='conc_1', offset=(2, 0, 0),
                             size=(input / 32, input / 32), n_filter=512,  conn=False, label=False)
    arch += tikz.short_connection(of='conc_1', to='conv_60',
                                   options='pos=0.75')
        
    arch += blocks.sum(name='sum_1', prev='conv_60', offset=(2, 0, 0), conn=True, )
    # arch += tikz.short_connection('conv_61', 'sum_1', anchor_of='-near', anchor_to='')

    arch += blocks.upsample(name='up_1', prev='sum_1', offset=(2, 0, 0),
                             size=(input / 16, input / 16), n_filter=512,  conn=True)
    arch += blocks.conv_relu(name='conv_62', prev='conv_60', offset=(2, 0, 13),
                             size=(input / 16, input / 16), n_filter=512,  conn=False, label=False)
    # arch += tikz.short_connection(of='conv_60', to='sum_1')

    # arch += tikz.z_conv_relu(name='conv_63', to='bottleneck_8_connection', offset=(0, 0, 8),
    #                        size=(input / 8, input / 8), n_filter=512)
    # arch += tikz.short_connection('bottleneck_8_connection', 'conv_63', anchor_of='', anchor_to='-far')
    arch += blocks.sum(name='sum_2', prev='up_1', offset=(2, 0, 0), conn=True)
    # arch += tikz.short_connection('conv_63', 'sum_2', anchor_of='-near', anchor_to='-northeast')
    # arch += tikz.short_connection('up_1', 'sum_2')

    arch += blocks.upsample(name='up_2', prev='sum_2', offset=(2, 0, 0),
                            size=(input / 8, input / 8), n_filter=512, anchor='-west')
    arch += tikz.conv_relu(name='conv_64', to='up_1-south', offset=(2, 0, 9),
                           size=(input / 8, input / 8), n_filter=512, label=False)
    arch += tikz.z_connection(of='up_1', to='conv_64', anchor_of='-nearsouth', anchor_to='-west', shift=(0.75, 0, 8.6))

    # arch += tikz.z_conv_relu(name='conv_65', to='bottleneck_4_connection', offset=(-0.25, 0, 10),
    #                        size=(input / 4, input / 4), n_filter=512)
    # arch += tikz.short_connection('bottleneck_4_connection', 'conv_65', anchor_of='', anchor_to='-far', options='pos=0.6')
    arch += blocks.sum(name='sum_3', prev='up_2', offset=(2, 0, 0), conn=True)
    # arch += tikz.short_connection('conv_65', 'sum_3', anchor_of='-near', anchor_to='-northeast')
    # arch += tikz.short_connection('up_2', 'sum_3')

    arch += tikz.conv_relu(name='conv_66', to='up_2-nearsouthwest', offset=(2, 0, 2),
                           size=(input / 4, input / 4), n_filter=512, label=False)
    arch += tikz.z_connection(of='up_2', to='conv_66', anchor_of='-nearsouthwest', anchor_to='-west', shift=(0.3, 0, 2.1))

    arch += tikz.conv_relu(name='conv_67', to='sum_3-east', offset=(1.5, 0, 0),
                           size=(input / 4, input / 4), n_filter=512, label=False)
    arch += tikz.short_connection(of='sum_3', to='conv_67')

    arch += blocks.conc(name='conc_2', prev='conv_66', offset=(4, 0, 0))


    arch += tikz.z_connection(of='conv_60', to='conv_62', anchor_of='-neareast', shift=(1, 0, 13))
    arch += tikz.z_connection(of='conv_62', to='conc_2', anchor_of='-east', anchor_to='-south', shift=(17, 0, 0))
    arch += tikz.z_connection(of='conv_64', to='conc_2', anchor_of='-east', anchor_to='-southwest', shift=(10.5, 0, 0))
    arch += tikz.z_connection(of='conv_66', to='conc_2', anchor_of='-east', anchor_to='-west', shift=(0, 0, 0))
    arch += tikz.z_connection(of='conv_67', to='conc_2', anchor_of='-east', anchor_to='-north', shift=(2, 0, 0))

    arch += tikz.coordinate('dummy_bn_1', 'sum_1-east', (-1.5, 0, -10))
    arch += tikz.coordinate('dummy_bn_2', 'sum_2-east', (-1.5, 0, -10))
    arch += tikz.coordinate('dummy_bn_3', 'sum_3-east', (-1.5, 0, -10))
    arch += tikz.short_connection('dummy_bn_1', 'sum_1', anchor_of='', anchor_to='-north')
    arch += tikz.short_connection('dummy_bn_2', 'sum_2', anchor_of='', anchor_to='-north')
    arch += tikz.short_connection('dummy_bn_3', 'sum_3', anchor_of='', anchor_to='-north')
    arch += tikz.z_connection('input', 'dummy_bn_3', anchor_of='', anchor_to='', shift=(0, 0, -10))




    
    # arch += tikz.coordinate('dummy_bn_4', 'sum_4-east', (0, 0, 0))

    # arch += tikz.z_connection(of='conc_2', to='conv_67', anchor_of='-southwest', shift=(0, 0, 7.1))

    # arch += tikz.short_connection(of='conv_62', to='conc_2', anchor_of='-east', anchor_to='-south')
    # arch += tikz.z_connection(of='up_3', to='conc_2', anchor_of='-far', anchor_to='-northwest', shift=(0, 0, 6))

    arch += blocks.conv_relu(name='conv_67_2', prev='conc_2', n_filter=512, size=(input / 4,
                             input / 4), offset=(2, 0, 0), conn=True, label=False)

    arch += blocks.conv_relu(name='conv_68', prev='conv_67_2', n_filter='27', width=2,
                             size=(input / 4, input / 4), offset=(3.5, 0, 0), label=False)
    arch += tikz.soft_max('soft_max', offset=(2, 0, 0), to='conv_68', size=(input / 4, input / 4),
                          n_filter=1)
    arch += tikz.short_connection('conv_68', 'soft_max')    
    arch += tikz.results_upsampling()
    # arch += tikz.spatial_mask()
    arch += tikz.legend()
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
