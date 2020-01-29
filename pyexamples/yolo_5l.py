import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *
from pycore.execute import *


# TODO:
#   fix (east-east) connections 108
#   fix \\
#   fix missing east block 108
#   fix 83 of 106
#   scale of long connections
#   documentation python code
#   documentation LaTeX code
#   \node[canvas is zy plane at x=16] (image2) at (3,0,9) {\includegraphics[width=2cm,height=2cm]{../examples/fcn8s/cats.jpg}};

def creatArchitecture():
    input = 40
    arch = []
    arch += to_Start()
    arch += to_Image(name='image_0', file='\\input_image', to=('-4,0,0'), size=[10, 10])
    arch += to_ConvRelu(name='conv_0', s_filter='I', size=(input, input), caption='0', n_filter=32)
    arch += to_ShortConnection(of='image_0', to='conv_0', anchor_of='', anchor_to='-west')
    arch += [*block_MultiConvRelu(num=3, name='conv', prev='conv_0', layer_num=1, name_start=1, n_filter=[64, 32, 64], s_filter='I/2', offset = '(3,0,0)', scale=16, size=(input/2, input/2), conn=True)]
    arch += to_Resample('conv_0', 'conv_1')
    # shortcut1
    arch += [*block_Shortcut(name='short_4', prev='conv_3', offset='(1.75,0,0)', size=(input/2, input/2), caption='4'),
    to_ShortConnection(of='conv_3', to='short_4'), to_LongConnection('conv_1', 'short_4', pos=1.3, anchor_to='-northwest')]
    arch += block_MultiConvRelu(num=3, name='conv', prev='short_4', layer_num=5, name_start=5, n_filter=[128, 64, 128], size=(input/4, input/4), conn=True, offset='(1.5,0,0)')
    # downsample
    arch += to_Resample(of='short_4', to='conv_5')
    arch += [*block_Shortcut(name='short_8', prev='conv_7', size=(input/4, input/4), caption='8', s_filter='I/4'), to_LongConnection('conv_5', 'short_8', pos=1.5), to_ShortConnection(of='conv_7', to='short_8')]
    # check in cfg
    arch += [*block_Shortcut(name='short_11', prev='short_8', size=(input/8, input/8), caption='11', s_filter='I/8')]
    # arch += [*block_ConvRelu(name='conv_12', prev='short_8', s_filter='I/8', n_filter=(256), size=(input/8, input/8), caption='12')]
    arch += to_Ellipsis(of='short_8', to='short_11')
    # arch += [*block_ConvRelu(name='conv_37', prev='conv_19', s_filter='I/16', n_filter=(512), size=(input/16, input/16), caption='37')]
    arch += [*block_Shortcut(name='short_36', prev='short_11', size=(input/16, input/16), caption='36')]
    arch += to_Ellipsis(of='short_11', to='short_36')
    arch += [*block_Shortcut(name='short_61', prev='short_36', size=(input/32, input/32), caption='61')]
    # arch += [*block_ConvRelu(name='short_61', prev='conv_37', s_filter='I/32', n_filter=(1024), size=(input/32, input/32))]
    arch += to_Ellipsis(of='short_36', to='short_61')
    # first yolo layer
    arch += [*block_ConvRelu(name='conv_79', prev='short_61', n_filter=(512), size=(input/32, input/32), caption='79')]
    arch += to_Ellipsis(of='short_61',to='conv_79')
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_79', layer_num=80, name_start=80,
    n_filter=[512, 1024, 256], s_filter='I/32', size=(input/32, input/32), conn=True, offset=3)]
    arch += [*block_Yolo(name='yolo_83', prev='conv_82', n_filter=(256), size=(input/32, input/32), caption='83', offset='(-0.75, 0, 3)', image=True, conn=True, grid=True)]
    # resample
    arch += [*block_ConvRelu(name='conv_85', prev='conv_79', n_filter=(256), offset='(1,0,0)', size=(input/32, input/32), caption='85', conn =True)]
    arch += [*block_Upsample(name='conv_86', prev='conv_85', s_filter='I/16', n_filter=(256), offset='(1,0,0)', size=(input/32, input/32), caption='86', conn=True)]
    # arch += to_Resample(of='conv_84', to='conv_84')
    arch += [*block_Conc(name='conc_87', prev='conv_86', offset='(1.25,0,0)')]
    arch += to_LongConnection(of='short_61', to= 'conc_87', pos=3)
    # second yolo layer
    arch += [*block_ConvRelu(name='conv_90', prev='conc_87', n_filter=(512), size=(input/16, input/16), caption='90')]
    arch += to_Ellipsis(of='conc_87', to='conv_90')
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_90', layer_num=91, name_start=91,
    n_filter=[256, 512, 256], s_filter='I/16', size=(input/16, input/16), conn=True, offset=3)]
    arch += [*block_Yolo(name='yolo_94', prev='conv_93', n_filter=(256), size=(input/16, input/16), caption='94', offset='(-0.75, 0, 3)', image=True, conn=True, grid=True)]
    # resample
    arch += [*block_ConvRelu(name='conv_96', prev='conv_90', n_filter=(128), offset='(1,0,0)', size=(input/16, input/16), caption='96', conn =True)]
    arch += [*block_Upsample(name='conv_97', prev='conv_96', s_filter='I/8', n_filter=(128), offset='(1,0,0)', size=(input/16, input/16), caption='97', conn=True)]
    # arch += to_Resample(of='conv_97', to='conv_96')
    arch += [*block_Conc(name='conc_98', prev='conv_97', offset='(1.25,0,0)')]
    arch += to_LongConnection(of='short_36', to='conc_98', pos=3.25)
    # third yolo layer
    arch += [*block_ConvRelu(name='conv_102', prev='conc_98', n_filter=(512), size=(input/8, input/8), caption='103')]
    arch += to_Ellipsis(of='conc_98', to='conv_102')
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_102', layer_num=103, name_start=103,
    n_filter=[128, 256, 256], s_filter='I/8', size=(input/8, input/8), conn=True, offset=4)]
    arch += [*block_Yolo(name='yolo_106', prev='conv_105', n_filter=(256), size=(input/8, input/8), caption='106', offset='(-1, 0, 4)', image=True, conn=True, grid=True)]
    # resample
    arch += [*block_ConvRelu(name='conv_108', prev='conv_102', n_filter=(128), offset='(1,0,0)', size=(input/8, input/8), caption='108', conn =True)]
    arch += [*block_Upsample(name='conv_109', prev='conv_108', s_filter='I/4', n_filter=(128), offset='(1,0,0)', size=(input/8, input/8), caption='109', conn=True)]
    # arch += to_Resample(of='conv_107', to='conv_108')
    arch += [*block_Conc(name='conc_110', prev='conv_109', offset='(1.25,0,0)')]
    arch += to_LongConnection(of='short_11', to= 'conc_110', pos=3)
    # forth yolo layer
    arch += [*block_ConvRelu(name='conv_114', prev='conc_110', n_filter=(512), size=(input/4, input/4), caption='114')]
    arch += to_Ellipsis(of='conc_110', to='conv_114')
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_114', layer_num=115, name_start=115,
    n_filter=[64, 128, 256], s_filter='I/4', size=(input/4, input/4), conn=True, offset=6)]
    arch += [*block_Yolo(name='yolo_4', prev='conv_117', n_filter=(256), size=(input/4, input/4), caption='118', offset='(-0.75, 0, 6)', image=True, conn=True, grid=True, steps=13)]
    # resample
    arch += [*block_ConvRelu(name='conv_120', prev='conv_114', n_filter=(128), offset='(1,0,0)', size=(input/4, input/4), caption='120', conn =True)]
    arch += [*block_Upsample(name='conv_121', prev='conv_120', s_filter='I/2', n_filter=(128), offset='(1,0,0)', size=(input/4, input/4), caption='121', conn=True)]
    # arch += to_Resample(of='conv_120', to='conv_120')
    arch += [*block_Conc(name='conc_122', prev='conv_121', offset='(1.5,0,0)')]
    arch += to_LongConnection(of='short_4', to='conc_122', pos=1.5, anchor_of_1='-southeast', anchor_of_2='-northeast')
    # fith yolo layer
    arch += [*block_ConvRelu(name='conv_126', prev='conc_122', n_filter=(128), size=(input/2, input/2), caption='126', offset='(2,0,0)')]
    arch += to_Ellipsis(of='conc_122', to='conv_126')
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_126', layer_num=127, name_start=127,
    n_filter=[32, 64, 256], s_filter='I/2', size=(input/2, input/2), conn=True, offset=8)]
    arch += [*block_Yolo(name='yolo_130', prev='conv_129', n_filter=(256), size=(input/2, input/2), caption='130', offset='(-0.5, 0, 8)', image=True, conn=True, grid=True, steps=20)]
    # arch += block_Shortcut
    arch += to_Legend()
    # arch += [*block_Conv(name='conv_80', prev='conv_79', s_filter='I/32', n_filter=(512), offset='(1,0,1)', size=(1, 1), caption='80')]
    # arch += [*block_Conv(name='conv_81', prev='conv_80', s_filter='I/32', n_filter=(512), offset='(1,0,1)', size=(1, 1), caption='81')]
    arch += to_End()
    return arch


def main():
    try:
        namefile = str(sys.argv[0]).split('.')[0]
        arch = creatArchitecture()
        # to_Generate(arch, namefile + '.tex')
        content = buildArchitecture(arch)
        writeTex(content, namefile + ".tex")
        texToPDF(namefile + ".tex")
        openPDF("xdg-open", namefile + ".pdf")
    except:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == '__main__':
    main()
