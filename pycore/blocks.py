import pycore.tikz as tikz
from math import log


# define new block
def conv(name, prev='', s_filter='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0,
         caption=' ', conn=False, anchor='-east'):

    """
    Generate a convolution layer

    Arguments:
        name {str} -- layer name

   Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        offset {tuple} -- offset to previous layer (default: {(1,0,0)})
        size {tuple} -- size (default: {(32,32)})
        width {str} -- width of layers in graph (default: {'0'})
        caption {str} -- layer caption (default: {''})
        conn {bool} -- draw short connection from prev layer (default: {False})
        anchor {str} -- position of anchor (default: {'-east'})

    Returns:
        layer {list} -- list of graph elements
    """

    if not prev:
        # assuming that layer names are given in a uniform way with incrementing numbers
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.conv(
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
        layer += tikz.short_connection('{}'.format(prev), '{}'.format(name))
    return layer

def conv_pool(name, prev='', s_filter=256, n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0, caption='',
              conn=True, opacity=0.5, anchor='-east'):

    """
    Generate a convolution layer together with relu activation and pooling

    Arguments:
        name {str} -- layer name

   Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        offset {tuple} -- offset to previous layer (default: {(1,0,0)})
        size {tuple} -- size (default: {(32,32)})
        width {str} -- width of layers in graph (default: {'0'})
        caption {str} -- layer caption (default: {''})
        conn {bool} -- draw short connection from prev layer (default: {False})
        anchor {str} -- position of anchor (default: {'-east'})

    Returns:
        layer {list} -- list of graph elements
    """
    layer = tikz.conv_relu(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size,
    )
    layer += tikz.pool(
        name='{}'.format(name),
        offset=(0, 0, 0),
        to='{}-east'.format(name),
        width=1,
        height=size[0] - int(size[0] / 4),
        depth=size[1] - int(size[0] / 4),
        opacity=opacity
    )
    if conn:
        layer += tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    return layer


def multi_conv(num, name, prev, layer_num=0, s_filter=256, n_filter=64, scale=32, name_start=0, offset=(1, 0, 0),
               width='0', size=(32, 32), opacity=0.5, conn=False, anchor='-east'):

    """ 
    Generate a block of multiple convolution layers

    Arguments:
        num {[type]} -- [description]
        name {[type]} -- [description]
        prev {[type]} -- [description]

    Keyword Arguments:
        layer_num {int} -- [description] (default: {0})
        s_filter {int} -- [description] (default: {256})
        n_filter {int} -- [description] (default: {64})
        scale {int} -- [description] (default: {32})
        name_start {int} -- [description] (default: {0})
        offset {tuple} -- [description] (default: {(1, 0, 0)})
        width {str} -- [description] (default: {'0'})
        size {tuple} -- [description] (default: {(32, 32)})
        opacity {float} -- [description] (default: {0.5})
        conn {bool} -- [description] (default: {False})
        anchor {str} -- [description] (default: {'-east'})

    Returns:
        [type] -- [description]
    """

    layers = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    # first layer
    layer = [tikz.conv(
             name='{}'.format(layers[0]),
             caption=str(layer_num + j),
             offset=offset,
             to='{}{}'.format(prev, anchor),
             n_filter=n_filter[j],
             size=size,
             width=log(n_filter[j], 4)
             )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.short_connection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        layer = [tikz.conv(
            name='{}'.format(l_name),
            caption=str(layer_num + j),
            offset='(0,0,0)',
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
        )]
        prev = l_name
        layers += layer
        j += 1

    # last layer
    layer = [tikz.conv(
        name='{}'.format(layers[-1]),
        caption=str(layer_num + j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers

def multi_conv_z(num, name, prev, layer_num=0, s_filter=256, n_filter=64, name_start=0,
                 offset=(1, 0, 0), width='0', size=(32, 32), opacity=0.5, conn=False, anchor='-east'):
                 
    """
    Generate a block of multiple convolution layers along the z axis

    Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        name_start {int} -- number of the first layer, succeeding layers get incrementing numbers (default: {0})
        offset {tuple} -- offset between layers (default: {'(1,0,0)'})
        width {str} -- width of layers in graph (default: {'0'})
        size {tuple} -- [description] (default: {(32,32)})
        opacity {float} -- [description] (default: {0.5})
        conn {bool} -- [description] (default: {False})
        anchor {str} -- [description] (default: {'-east'})

    Returns:
        layers {list} -- list of graph elements
    """

    layers = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    # first layer
    layer = [tikz.conv(
        name='{}'.format(layers[0]),
        caption=str(layer_num + j),
        offset=offset,
        to='{}{}'.format(prev, anchor),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.long_connection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        layer = [tikz.conv(
            name='{}'.format(l_name),
            caption=str(layer_num + j),
            offset=offset,
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
        )]
        prev = l_name
        layers += layer
        j += 1
    # last layer
    layer = [tikz.conv(
        name='{}'.format(layers[-1]),
        caption=str(layer_num + j),
        offset=offset,
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers

def conv_relu(name, prev='', s_filter=256, n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0, 
              caption='', conn=False, anchor='-east'):

    """Generate convolution layer with relu activation

    Arguments:
        name {string} -- layer name

    Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        offset {tuple} -- offset to previous layer (default: {(1,0,0)})
        size {tuple} -- [description] (default: {(32,32)})        
        width {str} -- width of layers in graph (default: {'0'})
        caption {str} -- layer caption (default: {''})
        conn {bool} -- draw short connection from prev layer (default: {False})
        anchor {str} -- position of anchor (default: {'-east'})

    Returns:
        layer {list} -- list of graph elements
    """

    # if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.conv_relu(
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
        layer += tikz.short_connection('{}'.format(prev), '{}'.format(name))
    return layer


def multi_conv_relu(num, name, prev, layer_num=0, s_filter=256, n_filter=64, name_start=0, offset=(1, 0, 0),
                    width=0, size=(32, 32), opacity=0.5, conn=False, anchor='-east'):

    """Generate multiple convolution layers with relu activation

        Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        name_start {int} -- number of the first layer, succeeding layers get incrementing numbers (default: {0})
        offset {tuple} -- offset between layers (default: {(1,0,0)})
        width {int} -- width of layers in graph (default: {0})
        size {tuple} -- size (default: {(32,32)})
        opacity {float} -- opacity (default: {0.5})
        conn {bool} -- draw short connection from prev layer (default: {False})
        anchor {str} -- position of anchor (default: {'-east'})

    Returns:
        layers {list} -- list of graph elements
    """

    layers = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    # first layer
    layer = [tikz.conv_relu(
        name='{}'.format(layers[0]),
        caption=str(layer_num + j),
        offset=offset,
        to='{}{}'.format(prev, anchor),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.short_connection(prev, layers[0])
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        layer = [tikz.conv_relu(
            name='{}'.format(l_name),
            caption=str(layer_num + j),
            offset='(0,0,0)',
            to='{}{}'.format(prev, anchor),
            n_filter=n_filter[j],
            size=size,
            width=log(n_filter[j], 4)
        )]
        prev = l_name
        layers += layer
        j += 1
    # last layer
    layer = [tikz.conv_relu(
        name='{}'.format(layers[-1]),
        caption=str(layer_num + j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers


def multi_conv_relu_z(num, name, prev, layer_num=0, s_filter=256, n_filter='', name_start=0, offset=(1, 0, 0),
                      width='0', size=(32, 32), opacity=0.5, conn=False, anchor='-east'):

    """Generate multiple convolution layers with relu activation along the z axis

        Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        name_start {int} -- number of the first layer, succeeding layers get incrementing numbers (default: {0})
        offset {str} -- offset between layers (default: {(1,0,0)})
        width {str} -- width of layers in graph (default: {'0'})
        size {tuple} -- [description] (default: {(32,32)})
        opacity {float} -- [description] (default: {0.5})
        conn {bool} -- [description] (default: {False})
        anchor {str} -- [description] (default: {'-east'})

    Returns:
        layers {list} -- list of graph elements
    """

    layers = []
    j = 0
    layers = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if isinstance(offset, int):
        offset_str = '({},{},{})'.format(-(4 / offset), 0, offset)
    else:
        offset_str = offset
    # first layer
    layer = [tikz.conv_relu(
        name='{}'.format(layers[0]),
        offset=offset_str,
        to='{}{}'.format(prev, anchor),
        size=size,
        width=log(n_filter[j], 4)
    )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.short_connection(of=prev, to=layers[0], anchor_of='-near', anchor_to='-far')
    prev = layers[0]

    # middle layers
    for l_name in layers[1:-1]:
        layer = [tikz.conv_relu(
            name='{}'.format(l_name),
            offset=offset_str,
            to='{}{}'.format(prev, anchor),
            size=size,
            width=log(n_filter[j], 4)
        )]
        layers += layer
        j += 1
        if conn:
            layers += tikz.short_connection(of=prev, to=l_name, anchor_of='-near', anchor_to='-far')
        prev = l_name
    # last layer
    layer = [tikz.conv_relu(
        name='{}'.format(layers[-1]),
        caption=str(layer_num + j),
        offset=offset_str,
        to='{}{}'.format(prev, anchor),
        s_filter=str(s_filter),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    if conn:
        layers += tikz.short_connection(of=prev, to=layers[-1], anchor_of='-near', anchor_to='-far')
    return layers


def upsample(name, prev='', s_filter=256, n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0, opacity=0.5,
             caption='', conn=False, anchor='-east'):

    """
    Generate upsampling layer

    Arguments:
        name {str} -- layer name

    Keyword Arguments:
        prev {string} -- name of previous layer
        s_filter {int} -- size of the the filters (default: {256})
        n_filter {int} -- number of filters (default: {64})
        offset {str} -- offset between layers (default: {(1,0,0)})
        size {tuple} -- size (default: {(32,32)})
        width {int} -- width of layers in graph (default: {0})
        opacity {float} -- opacity (default: {0.5})
        caption {str} -- layer caption (default: {''})
        opacity {float} -- opacity (default: {0.5})
        conn {bool} -- draw short connection from prev layer (default: {False})
        anchor {str} -- position of anchor (default: {'-east'})

    Returns:
        layer {list} -- list of graph elements
    """

    # if names are equal with incrementing numbers, assume name
    if not prev:
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.upsample(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size_1=size,
        size_2=(2 * size[0], 2 * size[1]),
    )
    if conn:
        layer += tikz.short_connection(prev, '{}_0'.format(name))
    return layer


def block_unconv(name, bottom, top, s_filter=256, n_filter=64, offset=(1, 0, 0), size=(32, 32, 3.5), opacity=0.5):
    layers = tikz.unpool(
        name='unpool_{}'.format(name), offset=offset, to='({}-east)'.format(bottom),
        width=1, height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv_res(
        name='ccr_res_{}'.format(name), offset='(0,0,0)', to='(unpool_{}-east)'.format(name),
        s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv(
        name='ccr_{}'.format(name), offset='(0,0,0)', to='(ccr_res_{}-east)'.format(name),
        s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1])
    layers += tikz.conv_res(
        name='ccr_res_c_{}'.format(name), offset='(0,0,0)', to='(ccr_{}-east)'.format(name),
        s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv(
        name='{}'.format(top), offset='(0,0,0)', to='(ccr_res_c_{}-east)'.format(name),
        s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1])
    layers += tikz.short_connection(
        '{}'.format(bottom),
        'unpool_{}'.format(name)
    )
    return layers


def res(num, name, bottom, top, start_no=0, s_filter=256, n_filter=64,
        offset=(0, 0, 0), size=(32, 32, 3.5), opacity=0.5):
    layers = []
    layers = [*['{}_{}'.format(name, i)for i in range(num - 1)], top]
    for name in layers:
        layer = [tikz.conv(
            name='{}'.format(name),
            offset=offset,
            to='{}-east'.format(bottom),
            s_filter=str(s_filter),
            n_filter=str(n_filter),
            width=size[2],
            height=size[0],
            depth=size[1]),
            tikz.short_connection(
                '{}'.format(bottom),
                '{}'.format(name))
        ]
        bottom = name
        layers += layer

    layers += [
        tikz.skip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return layers

def shortcut(name, prev, offset=(1, 0, 0), size=[40, 40], anchor='-east', caption='', s_filter=''):
    return [
        tikz.shortcut(
            name='{}'.format(name),
            s_filter=str(s_filter),
            to='{}{}'.format(prev, anchor),
            offset='{}'.format(offset),
            caption=caption,
            size=size
        )
    ]


def sum(name, prev, offset=(1, 0, 0)):
    return [
        tikz.add(
            name='{}'.format(name),
            to='{}'.format(prev),
            offset='{}'.format(offset)
        ),
        tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    ]

def mult(name, prev, offset=(1, 0, 0)):
    return [
        tikz.multiply(
            name='{}'.format(name),
            to='{}'.format(prev),
            offset='{}'.format(offset)
        ),
        tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    ]

def conc(name, prev, offset=(1, 0, 0)):
    return [
        tikz.concatenate(
            name='{}'.format(name),
            to='{}'.format(prev),
            offset='{}'.format(offset)
        ),
        tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    ]

def yolo(name, prev='', s_filter='', n_filter=64, offset='(-1,0,4)', size=[32, 32], width=1, scale=32,
         caption=' ', conn=False, anchor='-east', image=False, path='\\input_image', grid=False, steps=1):
    if not prev:
        # if names are equal with incrementing numbers, assume name
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.detect(
        name='{}'.format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size
    )
    if image:
        layer += image('image_{}'.format(name), path, to=(name + anchor), size=[(size[0] / 5), (size[1] / 5)])
    if grid:
        layer += grid('grid_{}'.format(name), 'image_{}'.format(name), size=[(size[0] / 5), (size[1] / 5)], steps=steps)
    if conn:
        layer += tikz.short_connection('{}'.format(prev), '{}'.format(name), anchor_of='-near', anchor_to='-far')
    return layer
