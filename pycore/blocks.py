from .tikzeng import *
from math import log


# define new block
def block_2ConvPool(name, bottom, top, s_filter=256, n_filter=64, offset='(1,0,0)', size=(32, 32, 3.5), opacity=0.5):
    return [
    to_ConvRelu(
        name='ccr_{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter, n_filter),
        offset=offset,
        to='{}-east'.format(bottom),
        width=(size[2], size[2]),
        height=size[0],
        depth=size[1],
       ),
    to_Pool(
        name='{}'.format(top),
        offset='(0,0,0)',
        to='ccr_{}-east'.format(name),
        width=1,
        height=size[0] - int(size[0]/4),
        depth=size[1] - int(size[0]/4),
        opacity=opacity,),
    to_ShortConnection(
        '{}'.format(bottom),
        'ccr_{}'.format(name)
       )
    ]


def block_Conv(name, prev='', s_filter='', n_filter=64, offset='(1,0,0)', size=(32, 32), width=0, scale=32, caption=' ', conn=False, anchor='-east'):
# if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1])-1))
    if not width:
        width = log(n_filter,4)
    layer = to_Conv(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size,
       )
    if conn:
        layer += to_ShortConnection('{}'.format(prev),'{}'.format(name))
    return layer


def block_MultiConv(num, name, prev, layer_num=0, s_filter=256, n_filter=64, scale=32, name_start=0, offset='(1,0,0)', width= '0', size=(32,32), opacity=0.5, conn=False, anchor='-east'):
    lys = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num+name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter]*num
    # first layer
    ly = [to_Conv(
            name='{}'.format(layers[0]),
            caption=str(layer_num+j),
            offset=offset,
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
    j += 1
    lys = ly
    if conn:
        lys += to_ShortConnection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        ly = [to_Conv(
            name='{}'.format(l_name),
            caption=str(layer_num+j),
            offset='(0,0,0)',
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
        prev = l_name
        lys += ly
        j += 1
    # last layer
    ly = [to_Conv(
        name='{}'.format(layers[-1]),
        caption=str(layer_num+j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
        )]
    lys += ly
    return lys

def block_MultiConvZ(num, name, prev, layer_num=0, s_filter=256, n_filter=64, scale=32, name_start=0, offset='(1,0,0)', width= '0', size=(32,32), opacity=0.5, conn=False, anchor='-east'):
    lys = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num+name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter]*num
    # first layer
    ly = [to_Conv(
            name='{}'.format(layers[0]),
            caption=str(layer_num+j),
            offset=offset,
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
    j += 1
    lys = ly
    if conn:
        lys += to_LongConnection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        ly = [to_Conv(
            name='{}'.format(l_name),
            caption=str(layer_num+j),
            offset=offset,
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
        prev = l_name
        lys += ly
        j += 1
    # last layer
    ly = [to_Conv(
        name='{}'.format(layers[-1]),
        caption=str(layer_num+j),
        offset=offset,
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
        )]
    lys += ly
    return lys

def block_ConvRelu(name, prev='', s_filter='', n_filter=64, offset='(1,0,0)', size=(32, 32), width=0, scale=32, caption=' ', conn=False, anchor='-east'):
# if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1])-1))
    if not width:
        width = log(n_filter,4)
    layer = to_ConvRelu(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size,
       )
    if conn:
        layer += to_ShortConnection('{}'.format(prev),'{}'.format(name))
    return layer


def block_MultiConvRelu(num, name, prev, layer_num=0, s_filter='', n_filter=64, scale=32, name_start=0, offset='(1,0,0)', width= '0', size=(32,32), opacity=0.5, conn=False, anchor='-east'):
    lys = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num+name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter]*num
    # first layer
    ly = [to_ConvRelu(
            name='{}'.format(layers[0]),
            caption=str(layer_num+j),
            offset=offset,
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
    j += 1
    lys = ly
    if conn:
        lys += to_ShortConnection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        ly = [to_ConvRelu(
            name='{}'.format(l_name),
            caption=str(layer_num+j),
            offset='(0,0,0)',
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
            )]
        prev = l_name
        lys += ly
        j += 1
    # last layer
    ly = [to_ConvRelu(
        name='{}'.format(layers[-1]),
        caption=str(layer_num+j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
        )]
    lys += ly
    return lys


def block_MultiConvReluZ(num, name, prev, layer_num=0, s_filter='', n_filter=64, scale=32, name_start=0, offset='(1,0,0)', width= '0', size=(32,32), opacity=0.5, conn=False, anchor='-east'):
    lys = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num+name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter]*num
    if isinstance(offset, int):
        offset_str = '({},{},{})'.format(-(4/offset), 0, offset)
    else:
        offset_str = offset
    # first layer
    ly = [to_ConvRelu(
            name='{}'.format(layers[0]),
            offset=offset_str,
            to='{}{}'.format(prev, anchor),
            size=size,
            width=log(n_filter[j], 4)
            )]
    j += 1
    lys = ly
    if conn:
        lys += to_ShortConnection(of=prev, to=layers[0], anchor_of='-near', anchor_to='-far')
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        ly = [to_ConvRelu(
            name='{}'.format(l_name),
            offset=offset_str,
            to='{}{}'.format(prev, anchor),
            size=size,
            width=log(n_filter[j], 4)
            )]
        lys += ly
        j += 1
        if conn:
            lys += to_ShortConnection(of=prev, to=l_name, anchor_of='-near', anchor_to='-far')
        prev = l_name
    # last layer
    ly = [to_ConvRelu(
        name='{}'.format(layers[-1]),
        caption=str(layer_num+j),
        offset=offset_str,
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
        )]
    lys += ly
    if conn:
        lys += to_ShortConnection(of=prev, to=layers[-1], anchor_of='-near', anchor_to='-far')
    return lys


def block_Upsample(name, prev='', s_filter='', n_filter=64, offset='(1,0,0)', size=(32, 32), width=0, scale=32, opacity=0.5, caption = ' ', conn=False, anchor='-east'):
# if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1])-1))
    if not width:
        width = log(n_filter,4)
    layer = to_Upsample(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size_1=size,
        size_2=(2*size[0], 2*size[1]),
       )
    if conn:
        layer += to_ShortConnection(prev, '{}_0'.format(name))
    return layer




def block_Unconv(name, bottom, top, s_filter=256, n_filter=64, offset='(1,0,0)', size=(32, 32, 3.5), opacity=0.5):
    return [
        to_UnPool(name='unpool_{}'.format(name), offset=offset, to='({}-east)'.format(bottom), width=1, height=size[0], depth=size[1], opacity=opacity),
        to_ConvRes(name='ccr_res_{}'.format(name), offset='(0,0,0)', to='(unpool_{}-east)'.format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='ccr_{}'.format(name), offset='(0,0,0)', to='(ccr_res_{}-east)'.format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1]),
        to_ConvRes(name='ccr_res_c_{}'.format(name), offset='(0,0,0)', to='(ccr_{}-east)'.format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='{}'.format(top), offset='(0,0,0)', to='(ccr_res_c_{}-east)'.format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1]),
        to_ShortConnection(
            '{}'.format(bottom),
            'unpool_{}'.format(name)
           )
    ]


def block_Res(num, name, bottom, top, start_no = 0, s_filter='', n_filter=64, offset='(0,0,0)', size=(32,32,3.5), opacity=0.5):
    lys = []
    layers = [*['{}_{}'.format(name,i)for i in range(num-1)], top]
    for name in layers:
        ly = [to_Conv(
            name='{}'.format(name),
            offset=offset,
            to='{}-east'.format(bottom),
            s_filter=str(s_filter),
            n_filter=str(n_filter),
            width=size[2],
            height=size[0],
            depth=size[1]
           ),
            to_ShortConnection(
                '{}'.format(bottom),
                '{}'.format(name)
               )
            ]
        bottom = name
        lys += ly

    lys += [
        to_Skip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys

def block_Shortcut(name, prev, offset='(1,0,0)', size=[40,40], anchor='-east', caption='', s_filter=''):
    return [
    to_Shortcut(
        name='{}'.format(name),
        s_filter=str(s_filter),
        to='{}{}'.format(prev, anchor),
        offset='{}'.format(offset),
        caption=caption,
        size=size
       ),
    ]


def block_Sum(name, prev, offset='(1,0,0)'):
    return [
    to_Add(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_ShortConnection(
        '{}'.format(prev),
        '{}'.format(name)
       )
    ]

def block_Mult(name, prev, offset='(1,0,0)'):
    return [
    to_Multiply(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_ShortConnection(
        '{}'.format(prev),
        '{}'.format(name)
       )
    ]

def block_Conc(name, prev, offset='(1,0,0)'):
    return [
    to_Concatenate(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_ShortConnection(
        '{}'.format(prev),
        '{}'.format(name)
       )
    ]

def block_Yolo(name, prev='', s_filter='', n_filter=64, offset='(-1,0,4)', size=[32, 32], width=0, scale=32,
caption=' ', conn=False, anchor='-east', image=False, path='\\input_image', grid=False, steps=1):
# if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1])-1))
    if not width:
        width = log(n_filter, 4)
    layer = to_Detect(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=1,
        size=size
       )
    if image:
        layer += to_Image('image_{}'.format(name), path, to=name+anchor, size=[(size[0]/5), (size[1]/5)])
    if grid:
        layer += to_Grid('grid_{}'.format(name), 'image_{}'.format(name), size=[(size[0]/5), (size[1]/5)], steps=steps)
    if conn:
        layer += to_ShortConnection('{}'.format(prev), '{}'.format(name), anchor_of='-near', anchor_to='-far')
    return layer
