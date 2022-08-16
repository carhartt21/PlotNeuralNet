import pycore.tikz as tikz
from math import log


# define new block
def conv(name, prev='', z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0,
         caption=' ', conn=True, anchor='-east'):

    """
    Generate a convolution layer

    Arguments:
        name {str} -- layer name

   Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        z_label {str} -- label along the z axis of the layer (default: '')
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
    if not isinstance(size, tuple):
        size = (size, size)
    if not prev:
        # assuming that layer names are given in a uniform way with incrementing numbers
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.conv(
        name='{}'.format(name),
        z_label=z_label,
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

def conv_pool(name, prev='', z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0, caption='',
              conn=True, opacity=0.5, anchor='-east'):

    """
    Generate a convolution layer together with relu activation and pooling

    Arguments:
        name {str} -- layer name

   Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        z_label {str} -- label along the z axis of the layer (default: '')
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
    if not isinstance(size, tuple):
        size = (size, size)
    layer = tikz.conv_relu(
        name='{}'.format(name),
        z_label=z_label,
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size,
    )
    layer += tikz.pool(
        name='{}'.format(name),
        offset=(1, 0, 0),
        to='{}'.format(name),
        width=1,
        size=size,
        opacity=opacity
    )
    if conn:
        layer += tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    return layer


def multi_conv(num, name, prev, layer_num=0, z_label='', n_filter=64, scale=32, name_start=0, offset=(1, 0, 0),
               width='0', size=(32, 32), opacity=0.5, conn=True, anchor='-east'):

    """
    Generate a block of multiple convolution layers

    Arguments:
        num {[type]} -- [description]
        name {[type]} -- [description]
        prev {[type]} -- [description]

    Keyword Arguments:
        layer_num {int} -- [description] (default: {0})
        z_label {str} -- [description] (default: {256})
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
    layer_names = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if not isinstance(size, tuple):
        size = (size, size)
    # first layer
    layer = [tikz.conv(
             name='{}'.format(layer_names[0]),
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
        layers += tikz.short_connection(prev, layer_names[0])
    prev = layer_names[0]

    # middle layers
    for l_name in layer_names[1:-1]:
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
        name='{}'.format(layer_names[-1]),
        caption=str(layer_num + j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        z_label=z_label,
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers

def multi_conv_z(num, name, prev, layer_num=0, z_label='', n_filter=64, name_start=0,
                 offset=(1, 0, 0), width='0', size=(32, 32), opacity=0.5, conn=True, anchor='-east'):

    """
    Generate a block of multiple convolution layers along the z axis

    Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        z_label {str} -- label along the z axis of the layer (default: '')
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
    layer_names = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if not isinstance(size, tuple):
        size = (size, size)
    # first layer
    layer = [tikz.conv(
        name='{}'.format(layer_names[0]),
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
        layers += tikz.long_connection(prev, layer_names[0])
    prev = layer_names[0]

    # middle layers
    for l_name in layer_names[1:-1]:
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
        name='{}'.format(layer_names[-1]),
        caption=str(layer_num + j),
        offset=offset,
        to='{}{}'.format(prev, anchor),
        z_label=z_label,
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers

def conv_relu(name, prev='', z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0,
              caption='', conn=True, anchor='-east', anchor_to='-west', rtl=False, label=True):

    """Generate convolution layer with relu activation

    Arguments:
        name {string} -- layer name

    Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        z_label {str} -- label along the z axis of the layer (default: '')
        n_filter {int} -- number of filters (default: {64})
        offset {tuple} -- offset to previous layer (default: {(1,0,0)})
        size {int|tuple} -- [description] (default: {(32,32)})        
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
    if not isinstance(size, tuple):
        size = (size, size)
    if rtl:
        layer = tikz.rtl_conv_relu(
            name='{}'.format(name),
            z_label=z_label,
            n_filter=(n_filter),
            offset=offset,
            caption=caption,
            to='{}{}'.format(prev, anchor),
            width=width,
            size=size
        )
    else:   
        layer = tikz.conv_relu(
            name='{}'.format(name),
            z_label=z_label,
            n_filter=(n_filter),
            offset=offset,
            caption=caption,
            to='{}{}'.format(prev, anchor),
            width=width,
            size=size,
            label=label
        )
    if conn:
        layer += tikz.short_connection('{}'.format(prev), '{}'.format(name), anchor_of=anchor, anchor_to=anchor_to)
    return layer


def new_branch(name, prev='', z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0,
              caption='', conn=True, anchor='-near'):
    """Generate convolution layer with relu activation

    Arguments:
        name {string} -- layer name

    Keyword Arguments:
        prev {str} -- name of previous layer (default: {''})
        z_label {str} -- label along the z axis of the layer (default: '')
        n_filter {int} -- number of filters (default: {64})
        offset {tuple} -- offset to previous layer (default: {(1,0,0)})
        size {int|tuple} -- [description] (default: {(32,32)})        
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
    if not isinstance(size, tuple):
        size = (size, size)
    layer = tikz.conv_relu(
        name='{}'.format(name),
        z_label=z_label,
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size
    )
    if conn:
        layer += tikz.z_connection('{}'.format(prev), '{}'.format(name), z_shift=offset[-1], anchor_of=anchor)
    return layer


def multi_conv_relu(num, name, prev, layer_num=0, z_label='', n_filter=(64), name_start=0, offset=(1, 0, 0),
                    width=0, size=(32, 32), opacity=0.5, conn=True, anchor='-east'):

    """Generate multiple convolution layers with relu activation

        Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network for the caption (default: {0})
        z_label {str} -- label along the z axis of the layer (default: '')
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
    layer_names = [*['{}_{}'.format(name, i) for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if not isinstance(size, tuple):
        size = (size, size)
    # first layer
    layer = [tikz.conv_relu(
        name='{}'.format(layer_names[0]),
        caption=str(layer_num + j) if layer_num else '',
        offset=offset,
        to='{}{}'.format(prev, anchor),
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.short_connection(prev, layer_names[0])
    prev = layer_names[0]

    # middle layers
    for l_name in layer_names[1:-1]:
        layer = [tikz.conv_relu(
            name='{}'.format(l_name),
            caption=str(layer_num + j) if layer_num else '',
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
        name='{}'.format(layer_names[-1]),
        caption=str(layer_num + j) if layer_num else '',
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        z_label=z_label,
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    return layers


def bottleneck(num, name, prev, layer_num=0, z_label='', n_filter=64, name_start=0, offset=(1, 0, 0),
               width=0, size=(32, 32), opacity=0.5, conn=True, anchor='-east', ellipsis=False, pos=1.5):
    """Generate multiple convolution layers with relu activation

        Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        z_label {str} -- label along the z axis of the layer (default: '')
        n_filter {int} -- number of filters (default: {64})
        name_start {int} -- number of the first layer, succeeding layers get incrementing numbers (default: {0})
        offset {tuple} -- offset between layers (default: {(1,0,0)})
        width {int} -- width of layers in graph (default: {0})
        size {tuple} -- size (default: {(32,32)})
        opacity {float} -- opacity (default: {0.5})
        conn {bool} -- draw short connection from prev layer (default: {True})
        anchor {str} -- position of anchor (default: {'-east'})
        ellipsis {bool} -- draw an ellipsis before the first layer (default: {False})
        pos {int} -- position of the long connection (default: {1.5})

    Returns:
        layers {list} -- list of graph elements
    """

    layers = []
    j = 0
    prev_layer = prev
    layer_names = [*['{}_{}'.format(name, i) for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if not isinstance(size, tuple):
        size = (size, size)
    # first layer
    layer = [tikz.conv_relu(
        name='{}'.format(layer_names[0]),
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
        layers += tikz.short_connection(prev, layer_names[0], name='({}_connection)'.format(name), options='pos=0.55')
    if ellipsis:
        layers += tikz.ellipsis(prev, layer_names[0])
        layers += r'''
        \coordinate [shift={(-0.25,0,0)}] (''' + name + '''_connection) at (''' + layer_names[0] +'''-west);
        '''
    prev = layer_names[0]

    # middle layers
    for l_name in layer_names[1:-1]:
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
        name='{}'.format(layer_names[-1]),
        caption=str(layer_num + j),
        offset='(0,0,0)',
        to='{}{}'.format(prev, anchor),
        z_label=z_label,
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    prev = layer_names[-1]
    # layers += tikz.relu(
    #     name='{}_relu'.format(layer_names[-1]),
    #     to='{}{}'.format(prev, anchor),
    #     offset=(1, 0, 0),
    #     size=size)
    # layers += tikz.short_connection('{}'.format(layer_names[-1]), '{}_relu'.format(layer_names[-1]))
    layers += tikz.long_connection_reversed('{}'.format(layer_names[-1]), '{}_connection'.format(name), pos=pos, anchor_to='')
    return layers


def multi_conv_relu_z(num, name, prev, layer_num=0, z_label='', n_filter='', name_start=0, offset=(1, 0, 0),
                      width='0', size=(32, 32), opacity=0.5, conn=True, anchor='-east'):

    """Generate multiple convolution layers with relu activation along the z axis

        Arguments:
        num {int} -- number of layers
        name {string} -- block name
        prev {string} -- name of previous layer

    Keyword Arguments:
        layer_num {int} -- layer number in the network (default: {0})
        z_label {str} -- label along the z axis of the layer (default: '')
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
    layer_names = [*['{}_{}'.format(name, i)for i in range(name_start, num + name_start)]]
    if not isinstance(n_filter, list):
        n_filter = [n_filter] * num
    if isinstance(offset, int):
        offset_str = '({},{},{})'.format(-(4 / offset), 0, offset)
    else:
        offset_str = offset
    if not isinstance(size, tuple):
        size = (size, size)
    # first layer
    layer = [tikz.conv_relu(
        name='{}'.format(layer_names[0]),
        offset=offset_str,
        to='{}{}'.format(prev, anchor),
        size=size,
        width=log(n_filter[j], 4)
    )]
    j += 1
    layers = layer
    if conn:
        layers += tikz.short_connection(of=prev, to=layer_names[0], anchor_of='-near', anchor_to='-far')
    prev = layer_names[0]

    # middle layers
    for l_name in layer_names[1:-1]:
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
        name='{}'.format(layer_names[-1]),
        caption=str(layer_num + j),
        offset=offset_str,
        to='{}{}'.format(prev, anchor),
        z_label=z_label,
        n_filter=n_filter[j],
        size=size,
        width=log(n_filter[j], 4)
    )]
    layers += layer
    if conn:
        layers += tikz.short_connection(of=prev, to=layer_names[-1], anchor_of='-near', anchor_to='-far')
    return layers


def upsample(name, prev='', z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32), width=0, opacity=0.5,
             caption='', conn=True, anchor='-west', anchor_of='-east'):

    """
    Generate upsampling layer

    Arguments:
        name {str} -- layer name

    Keyword Arguments:
        prev {string} -- name of previous layer
        z_label {str} -- label along the z axis of the layer (default: '')
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
    if not isinstance(size, tuple):
        size = (size, size)
    layer = tikz.upsample(
        name='{}'.format(name),
        z_label=z_label,
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size_1=size,
        size_2=(2 * size[0], 2 * size[1]),
    )
    if conn:
        layer += tikz.short_connection(of=prev, to='{}_0'.format(name), anchor_of=anchor_of)
    return layer


def block_unconv(name, bottom, top, z_label='', n_filter=64, offset=(1, 0, 0), size=(32, 32, 3.5), opacity=0.5):
    layers = tikz.unpool(
        name='unpool_{}'.format(name), offset=offset, to='({}-east)'.format(bottom),
        width=1, height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv_res(
        name='ccr_res_{}'.format(name), offset='(0,0,0)', to='(unpool_{}-east)'.format(name),
        z_label=z_label, n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv(
        name='ccr_{}'.format(name), offset='(0,0,0)', to='(ccr_res_{}-east)'.format(name),
        z_label=z_label, n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1])
    layers += tikz.conv_res(
        name='ccr_res_c_{}'.format(name), offset='(0,0,0)', to='(ccr_{}-east)'.format(name),
        z_label=z_label, n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity)
    layers += tikz.conv(
        name='{}'.format(top), offset='(0,0,0)', to='(ccr_res_c_{}-east)'.format(name),
        z_label=z_label, n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1])
    layers += tikz.short_connection(
        '{}'.format(bottom),
        'unpool_{}'.format(name)
    )
    return layers


def res(num, name, bottom, top, start_no=0, z_label='', n_filter=64,
        offset=(0, 0, 0), size=(32, 32, 3.5), opacity=0.5):
    layers = []
    layer_names = [*['{}_{}'.format(name, i)for i in range(num - 1)], top]
    for name in layers:
        layer = [tikz.conv(
            name='{}'.format(name),
            offset=offset,
            to='{}-east'.format(bottom),
            z_label=z_label,
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
        tikz.skip(of=layer_names[1], to=layer_names[-2], pos=1.25),
    ]
    return layers

def shortcut(name, prev, offset=(1, 0, 0), size=[40, 40], anchor='-east', caption='', z_label='', conn=True):
    layer = tikz.shortcut(
        name='{}'.format(name),
        z_label=z_label,
        to='{}{}'.format(prev, anchor),
        offset='{}'.format(offset),
        caption=caption,
        size=size)
    if conn:
        layer += tikz.short_connection(of=prev, to=name)
    return layer


def sum(name, prev, offset=(1, 0, 0), conn=True):
    layer = tikz.add(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
    )
    if conn:
        layer += tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    return layer

def mult(name, prev, offset=(1, 0, 0), conn=True):
    layer = tikz.multiply(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
    )
    if conn:
        layer += tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    return layer


def conc(name, prev, offset=(1, 0, 0), conn=True):
    layer = tikz.concatenate(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
    )
    if conn:
        tikz.short_connection(
            '{}'.format(prev),
            '{}'.format(name)
        )
    return layer

def yolo(name, prev='', z_label='', n_filter=64, offset='(-1,0,4)', size=[32, 32], width=1, scale=32,
         caption=' ', conn=True, anchor='-east', image=False, path='\\input_image', grid=False, steps=1):
    if not prev:
        # if names are equal with incrementing numbers, assume name
        prev_s = name.split('_')
        prev = '{}_{}'.format(prev_s[0], str(int(prev_s[1]) - 1))
    if not width:
        width = log(n_filter, 4)
    layer = tikz.detect(
        name='{}'.format(name),
        z_label=z_label,
        n_filter=(n_filter),
        offset=offset,
        caption=caption,
        to='{}{}'.format(prev, anchor),
        width=width,
        size=size
    )
    if image:
        layer += tikz.image('image_{}'.format(name), path, to=(name + anchor), size=[(size[0] / 5), (size[1] / 5)])
    if grid:
        layer += tikz.grid('grid_{}'.format(name), 'image_{}'.format(name), size=[(size[0] / 5), (size[1] / 5)], steps=steps)
    if conn:
        layer += tikz.short_connection('{}'.format(prev), '{}'.format(name), anchor_of='-near', anchor_to='-far')
    return layer
