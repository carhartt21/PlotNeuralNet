import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *


# TODO:
#   documentation python code
#   documentation LaTeX code
#   \node[canvas is zy plane at x=16] (image2) at (3,0,9) {\includegraphics[width=2cm,height=2cm]{../examples/fcn8s/cats.jpg}};

def creatArchitecture(arch):
    input = 40
    arch += to_Start()
    arch += to_Input(pathfile='../examples/fcn8s/cats.jpg')
    arch += to_ConvRelu(name='conv_0', s_filter='I', size=(input, input), caption='0', n_filter=64)
    arch += block_MultiConvRelu(num=3, name='conv', prev='conv_0', layer_num=1, name_start=1, n_filter=[64, 32, 64], s_filter='I/2', scale=16, size=(input/2, input/2), conn=True)
    arch += to_Resample('conv_0', 'conv_1')
    # shortcut1
    arch += [*block_Sum(name='short_1', prev='conv_3', offset='(1.5,0,0)'), to_LongConnection('conv_1', 'short_1')]
    arch += block_MultiConvRelu(num=3, name='conv', prev='short_1', layer_num=4, name_start=4, n_filter=[128, 64, 128], s_filter='I/4', size=(input/4, input/4), conn=True)
    # downsample
    arch += to_Resample(of='conv_3', to='conv_4')
    arch += [*block_Sum(name='short_2', prev='conv_6'), to_LongConnection('conv_4', 'short_2')]
    arch += to_Ellipsis(name='e1', of='short_2', offset='(0.35, 0, 0)')
    arch += [*block_ConvRelu(name='conv_18', prev='e1', s_filter='I/8', n_filter=(256), offset='(0.35,0,0)', size=(input/8, input/8), caption='18', anchor='')]
    arch += to_Ellipsis(name='e2', of='conv_18', offset='(0.4, 0, 0)')
    arch += [*block_ConvRelu(name='conv_36', prev='e2', s_filter='I/16', n_filter=(512), offset='(0.4,0,0)', size=(input/16, input/16), caption='36', anchor='')]
    arch += to_Ellipsis(name='e3', of='conv_36', offset='(0.4, 0, 0)')
    arch += [*block_ConvRelu(name='conv_61', prev='e3', s_filter='I/32', n_filter=(1024), offset='(0.4,0,0)', size=(input/32, input/32), caption='61', anchor='')]
    arch += to_Ellipsis(name='e4', of='conv_61', offset='(0.4,0,0)')
    # first yolo layer
    arch += [*block_ConvRelu(name='conv_79', prev='e4', n_filter=(512), offset='(0.4,0,0)', size=(input/32, input/32), caption='79', anchor='')]
    arch += [*block_MultiConvReluZ(num=3, name='conv', prev='conv_79', layer_num=80, name_start=80,
    n_filter=[256, 1024, 256], s_filter='I/32', size=(input/32, input/32), conn=True, offset='(-0.5,0,3)')]
    arch += [*block_ConvRelu(name='conv_83', prev='conv_79', n_filter=(256), offset='(1,0,0)', size=(input/32, input/32), caption='83', conn =True)]
    arch += to_Upsample(name='conv_84', to='conv_83-east', s_filter='I/16', n_filter=(256), offset='(1,0,0)', size=(input/16, input/16), caption='84')
    arch += to_Resample(of='conv_83', to='conv_84')
    arch += [*block_Conc(name='conc_1', prev='conv_84', offset='(1,0,0)')]
    arch += to_LongConnection(of='conv_36', to= 'conc_1')
    #
    # arch += block_Sum

    # arch += [*block_Conv(name='conv_80', prev='conv_79', s_filter='I/32', n_filter=(512), offset='(1,0,1)', size=(1, 1), caption='80')]
    # arch += [*block_Conv(name='conv_81', prev='conv_80', s_filter='I/32', n_filter=(512), offset='(1,0,1)', size=(1, 1), caption='81')]
    arch += to_End()
    return arch


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = []
    creatArchitecture(arch)
    to_Generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
