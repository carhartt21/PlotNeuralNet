from .tikzeng import *


# define new block
def block_2ConvPool(name, bottom, top, s_filter=256, n_filter=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return [
    to_ConvRelu(
        name="ccr_{}".format(name),
        s_filter=str(s_filter),
        n_filter=(n_filter, n_filter),
        offset=offset,
        to="({}-east)".format(bottom),
        width=(size[2], size[2]),
        height=size[0],
        depth=size[1],
       ),
    to_Pool(
        name="{}".format(top),
        offset="(0,0,0)",
        to="(ccr_{}-east)".format(name),
        width=1,
        height=size[0] - int(size[0]/4),
        depth=size[1] - int(size[0]/4),
        opacity=opacity,),
    to_short_connection(
        "{}".format(bottom),
        "ccr_{}".format(name)
       )
    ]


def block_Unconv(name, bottom, top, s_filter=256, n_filter=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return [
        to_UnPool(name='unpool_{}'.format(name), offset=offset, to="({}-east)".format(bottom), width=1, height=size[0], depth=size[1], opacity=opacity),
        to_ConvRes(name='ccr_res_{}'.format(name), offset="(0,0,0)", to="(unpool_{}-east)".format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='ccr_{}'.format(name), offset="(0,0,0)", to="(ccr_res_{}-east)".format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1]),
        to_ConvRes(name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='{}'.format(top), offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filter=str(s_filter), n_filter=str(n_filter), width=size[2], height=size[0], depth=size[1]),
        to_short_connection(
            "{}".format(bottom),
            "unpool_{}".format(name)
           )
    ]


def block_Res(num, name, bottom, top, s_filter=256, n_filter=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5):
    lys = []
    layers = [*['{}_{}'.format(name,i)for i in range(num-1)], top]
    for name in layers:
        ly = [to_Conv(
            name='{}'.format(name),
            offset=offset,
            to="({}-east)".format(bottom),
            s_filter=str(s_filter),
            n_filter=str(n_filter),
            width=size[2],
            height=size[0],
            depth=size[1]
           ),
            to_short_connection(
                "{}".format(bottom),
                "{}".format(name)
               )
            ]
        bottom = name
        lys += ly

    lys += [
        to_skip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


def sum(name, prev, offset="(1,0,0)"):
    return [
    to_add(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_short_connection(
        "{}".format(prev),
        "{}".format(name)
       )
    ]

def mult(name, prev, offset="(1,0,0)"):
    return [
    to_multiply(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_short_connection(
        "{}".format(prev),
        "{}".format(name)
       )
    ]

def conc(name, prev, offset="(1,0,0)"):
    return [
    to_concatenate(
        name='{}'.format(name),
        to='{}'.format(prev),
        offset='{}'.format(offset)
       ),
    to_short_connection(
        "{}".format(prev),
        "{}".format(name)
       )
    ]
