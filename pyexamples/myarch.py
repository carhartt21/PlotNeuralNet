import sys
from pycore.tikzeng import *
from pycore.blocks import *
sys.path.append('../')


# TODO:
#   documentation python code
#   documentation LaTeX code


def creatArchitecture(arch):
    input = 40
    arch += to_Start()
    arch += to_Input('../examples/fcn8s/cats.jpg')
    arch += to_Conv(name='conv_1', s_filter='I', size=(input, input), caption='1', n_filter=64)
    arch += block_MultiConv(num=3, name='conv', prev='conv_1', layer_num=2, name_start=2, n_filter=[64, 32, 64], s_filter='I/2', scale=16, size=((input/2), (input/2)), conn=True)
    arch += to_Resample('conv_1', 'conv_2')
    #shortcut
    arch += [*sum(name='short_1', prev='conv_4'), to_LongConnection('conv_2', 'short_1')]
    arch += block_MultiConv(num=3, name='conv', prev='short_1', layer_num=5, name_start=5, n_filter=[128, 64, 128], s_filter='I/4', size=((input/4), (input/4)), conn=True)
    arch += to_Resample(of='conv_4', to='conv_5')
    arch += [*sum(name='short_2', prev='conv_7'), to_LongConnection('conv_5', 'short_2')]
    arch += to_End()
    return arch


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = []
    creatArchitecture(arch)
    to_Generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
